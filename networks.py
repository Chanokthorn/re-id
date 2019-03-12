"""
    TO-DO
    -----
    - Define at least one embedding network
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from functools import reduce
from torchvision import models
from torch.nn import init


#<!-- START TEMPLATE NETWORKS --!>
class BaseNetwork(nn.Module):
    def __init__(self):
        super(BaseNetwork, self).__init__()
    
    def forward(self, *input):
        raise NotImplementedError
    
    def get_embedding(self, *input):
        """
            This method will be used to get all dataset result, and return it as torch.Tensor.
            This could be the same as forward method but was seperate to make it more semantic.
            And is for single input (unlike forward in TripletNet below).
        """
        raise NotImplementedError
    
class TripletNet(BaseNetwork):
    def __init__(self, embedding_net):
        super(TripletNet, self).__init__()
        self.embedding_net = embedding_net

    def forward(self, x1, x2, x3):
        output1 = self.embedding_net(x1)
        output2 = self.embedding_net(x2)
        output3 = self.embedding_net(x3)
        return output1, output2, output3

    def get_embedding(self, x):
        return self.embedding_net(x)

class QuintupletNet(BaseNetwork):
    def __init__(self, embedding_net):
        super(QuintupletNet, self).__init__()
        self.embedding_net = embedding_net

    def forward(self, x1, x2, x3, x4, x5):
        output1 = self.embedding_net(x1)
        output2 = self.embedding_net(x2)
        output3 = self.embedding_net(x3)
        output4 = self.embedding_net(x4)
        output5 = self.embedding_net(x5)
        return output1, output2, output3, output4, output5

    def get_embedding(self, x):
        return self.embedding_net(x)

# <!-- END TEMPLATE NETWORKS --!>

#<!-- START HELPER NETWORKS --!>
class STN(nn.Module):
    """
        This code is a modified version of PyTorch Official Tutorial which can be found (here)[https://pytorch.org/tutorials/intermediate/spatial_transformer_tutorial.html]
    """
    def __init__(self, width, height, channel, structure_localization=[(8, 7), (10, 5)], structure_regression=[32]):
        super(STN, self).__init__()
        
        # Spatial transformer localization-network
        loc_seq = []
        in_channel = channel
        w, h, c = width, height, structure_localization[-1][0]
        for (ch, ker) in structure_localization:
            loc_seq += [
                nn.Conv2d(in_channel, ch, kernel_size=ker),
                nn.MaxPool2d(2, stride=2),
                nn.ReLU(True)
            ]
            in_channel = ch
            w, h = int(( w - 2*(ker//2) )//2), int(( w - 2*(ker//2) )//2)
        self.localization = nn.Sequential(* loc_seq)
        
        # Regressor for the 3 * 2 affine matrix
        fc_seq = []
        in_channel = c * w * h
        if len(structure_regression) > 0:
            for size in structure_regression:
                fc_seq += [
                    nn.Linear(in_channel, size),
                    nn.ReLU(True)
                ]
                in_channel = size

            self.fc_loc = nn.Sequential(
                * fc_seq,
                nn.Linear(structure_regression[-1], 3 * 2)
            )
        else:
            self.fc_loc = nn.Sequential(
                nn.Linear(in_channel, 3 * 2)
            )

        # Initialize the weights/bias with identity transformation
        self.fc_loc[-1].weight.data.zero_()
        self.fc_loc[-1].bias.data.copy_(torch.tensor([1, 0, 0, 0, 1, 0], dtype=torch.float))
    
    def _cal_size_(self):
        w, h, c = self.width, self.height, self.structure_localization[-1][0]
        for ch, kernel in self.structure_localization:
            w, h = int(( w - 2*(kernel//2) )//2), int(( w - 2*(kernel//2) )//2)
        return int(w), int(h), int(c)
            

    def forward(self, x):
        # transform the input
        xs = self.localization(x)
        xs = xs.view(-1, reduce(lambda acc, x: acc*x, xs.shape[1:]))
        theta = self.fc_loc(xs)
        theta = theta.view(-1, 2, 3)

        grid = F.affine_grid(theta, x.size())
        x = F.grid_sample(x, grid)
        return x
    
#<!-- END HELPER NETWORKS --!>

#<!-- START EMBEDDING NETWORKS --!>
def weights_init_kaiming(m):
    classname = m.__class__.__name__
    # print(classname)
    if classname.find('Conv') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_in') # For old pytorch, you may use kaiming_normal.
    elif classname.find('Linear') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_out')
        init.constant_(m.bias.data, 0.0)
    elif classname.find('BatchNorm1d') != -1:
        init.normal_(m.weight.data, 1.0, 0.02)
        init.constant_(m.bias.data, 0.0)

def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        init.normal_(m.weight.data, std=0.001)
        init.constant_(m.bias.data, 0.0)


class ClassBlock(nn.Module):
    def __init__(self, input_dim, class_num, droprate, relu=False, bnorm=True, num_bottleneck=512, linear=True, return_f = False, is_use_sigmoid = False):
        super(ClassBlock, self).__init__()
        self.return_f = return_f
        self.is_use_sigmoid = is_use_sigmoid
        add_block = []
        if linear:
            add_block += [nn.Linear(input_dim, num_bottleneck)]
        else:
            num_bottleneck = input_dim
        if bnorm:
            add_block += [nn.BatchNorm1d(num_bottleneck)]
        if relu:
            add_block += [nn.LeakyReLU(0.1)]
        if droprate>0:
            add_block += [nn.Dropout(p=droprate)]
        add_block = nn.Sequential(*add_block)
        add_block.apply(weights_init_kaiming)

        classifier = []
        classifier += [nn.Linear(num_bottleneck, class_num)]
        classifier = nn.Sequential(*classifier)
        classifier.apply(weights_init_classifier)

        self.add_block = add_block
        self.classifier = classifier
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        x = self.add_block(x)
        if self.return_f:
            f = x
            x = self.classifier(x)
            if is_use_sigmoid:
                x = self.sigmoid(x)
            return x,f
        else:
            x = self.classifier(x)
            if self.is_use_sigmoid:
                x = self.sigmoid(x)
            return x

# Define the ResNet50-based Model
class ft_net(nn.Module):

    def __init__(self, stn=None, class_num=2048, droprate=0.5):
        super(ft_net, self).__init__()
        model_ft = models.resnet50(pretrained=False)
        # avg pooling to global pooling
        model_ft.avgpool = nn.AdaptiveAvgPool2d((1,1))
        self.model = model_ft
        self.classifier = ClassBlock(class_num, class_num, droprate)
        self.stn = stn

    def forward(self, x):
        if self.stn is not None:
            x = self.stn(x)
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)
        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)
        x = self.model.avgpool(x)
        x = x.view(x.size(0), x.size(1))
        x = self.classifier(x)
        return x

class ft_net_embed_only(nn.Module):

    def __init__(self, stn=None, class_num=2048, droprate=0.5):
        super(ft_net_embed_only, self).__init__()
        model_ft = models.resnet50(pretrained=False)
        # avg pooling to global pooling
        model_ft.avgpool = nn.AdaptiveAvgPool2d((1,1))
        self.model = model_ft
        self.stn = stn

    def forward(self, x):
        if self.stn is not None:
            x = self.stn(x)
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)
        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)
        x = self.model.avgpool(x)
        x = x.view(x.size(0), x.size(1))
        return x
#<!-- END EMBEDDING NETWORKS --!>