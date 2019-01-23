
# coding: utf-8

# In[1]:


import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
from collections import defaultdict
from torch.utils.data import Dataset, DataLoader
import random
import sys
from sklearn import decomposition
import numpy as np
from tqdm import tqdm
from copy import deepcopy
import time
import os
import multiprocessing
import math
import threading
from random import shuffle, sample
from torch.optim import lr_scheduler
import torch.optim as optim
from torch.autograd import Variable
from utils import get_bar
import cv2
from torch.nn import init
from torchvision import models
from networks import TripletNet, STN, ft_net_embed_only, ft_net
from pkl import save_pkl, load_pkl
from dataset import MarketDataset


# In[2]:


def initModel():
    tag_device = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(tag_device)

    default_batch_size = 12 if tag_device == "cuda" else 2
    default_num_workers = 6 if tag_device == "cuda" else 1
    is_use_sigmoid = False
    feature_size = 2048
    stn = STN(224, 224, 3, structure_localization=[(8, 7), (10, 5), (20, 3), (30, 3)], structure_regression=[128, 64, 32])
    model = ft_net(stn=stn)
    a = torch.load("./weights/best_train.pth")
    model.load_state_dict(a['model'])
    model.cuda()
    model.eval()
    return model


# In[3]:


class Model:
    def __init__(self):
#         self.model = initModel()
        mean = torch.Tensor(np.array([0.49137255, 0.48235294, 0.44666667], dtype=np.float32))
        std = torch.Tensor(np.array([0.24705882, 0.24352941, 0.26156863], dtype=np.float32))

        self.transforms = torchvision.transforms.Compose([
            torchvision.transforms.ToPILImage(),
            torchvision.transforms.Resize((224, 224)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mean=mean, std=std),
        ])
#     def getEmbedding(self, img1):
#         return model(img1)
#     def getDistance(self, img1, img2):
#         distance = img1 - img2
#         return np.dot(img1, img2)
    def forward(self, img1):
        with torch.no_grad():
            transformed = self.transforms(img1)
            transformed = torch.unsqueeze(transformed, 0)
            transformed = transformed.cuda()
            result = self.model(transformed).cpu().numpy()
            del transformed
        return result
    def releaseModel(self):
        del self.model
        torch.cuda.empty_cache()
        return "success"
    def loadModel(self):
        self.model = initModel()
        return "success"


# In[5]:


# path = '../Market-1501-v15.09.15/bounding_box_train'
# cap = 10
# split = 0.80
# seed = 1082

# mean = torch.Tensor(np.array([0.49137255, 0.48235294, 0.44666667], dtype=np.float32))
# std = torch.Tensor(np.array([0.24705882, 0.24352941, 0.26156863], dtype=np.float32))

# transforms = torchvision.transforms.Compose([
#     torchvision.transforms.ToPILImage(),
#     torchvision.transforms.Resize((224, 224)),
#     torchvision.transforms.ToTensor(),
#     torchvision.transforms.Normalize(mean=mean, std=std),
# ])

# train_cap = int(cap*split)
# test_cap = max(cap - train_cap, 0)
# train_image = MarketDataset(
#     path=path,
#     split=split,
#     train=True,
#     seed=seed,
#     transforms=transforms,
#     cap=train_cap
# )

