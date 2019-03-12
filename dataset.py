"""
    TO-DO
    -----
    - Define Positive/Negative mining dataset with optional parameters for matching or randomizing
"""

import os
import cv2
import sys
import math
import torch
import random
import torchvision
import numpy as np
from PIL import Image
from tqdm import tqdm
from copy import deepcopy
import torch.nn.functional as F
from random import shuffle, sample
from itertools import combinations
from collections import defaultdict
from torchvision import transforms, utils
from torch.utils.data import Dataset, DataLoader

# Common setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cuda = device != "cpu"

default_batch_size = 16 if cuda else 1
default_num_workers = 4 if cuda else 1

class MarketDataset(Dataset):
    """
        This Dataset is to read image from pre-defined path
        split is ratio size of train split portion
        Return:
            - Image as numpy array
            - Label as int of id
    """
    def __init__(self, path="../Market-1501-v15.09.15/bounding_box_train", cap=-1, split=1.0, seed=31415, transforms=None, train=True):
        super(MarketDataset, self).__init__()
        self.path = path
        self.split = split
        self.cap = cap
        self.seed = seed
        self.train = train
        self.train_idx, self.test_idx, self.ids2files = self._process_files_list_()
        self.fileList = self._match_file_()
        self.transforms = transforms
        
    def _process_files_list_(self):
        grouping = defaultdict(lambda: [])
        total_length = 0
        for idx, file in enumerate(sorted(os.listdir(self.path))):
            if file == "Thumbs.db":
                continue
            grouping[int(file.split("_")[0])].append(file)
            total_length += 1
        length_grouping = []
        for idx in list(grouping.keys()):
            length_grouping.append((len(grouping[idx]), idx))
        tmp = sorted(length_grouping)[:]
        random.Random(self.seed).shuffle(tmp)
        # Split train/test
        train_amt = min(math.floor(total_length * self.split), total_length)
        acc_amt = 0
        train_idx = []
        test_idx = []
        for amt, idx in tmp:
            if acc_amt >= train_amt:
                test_idx.append(idx)
            else:
                acc_amt += amt
                train_idx.append(idx)
        return train_idx, test_idx, grouping
    
    def _match_file_(self):
        idxes = self.train_idx if self.train else self.test_idx
        fileList = []
        for idx in idxes:
            for i in range(len(self.ids2files[idx])):
                fileList.append((idx, i))
                
        random.Random(self.seed).shuffle(fileList)
        return fileList[:self.cap if 0 <= self.cap <= len(fileList) else len(fileList)]
    
    def _read_image_(self, filename):
        if self.transforms is not None:
            return self.transforms(cv2.imread(self.path + '/' + filename))
        return cv2.imread(self.path + '/' + filename)
    
    def __len__(self):
        return len(self.fileList)
    
    def __getitem__(self, idx):
        return self._read_image_(self.ids2files[self.fileList[idx][0]][self.fileList[idx][1]]), self.fileList[idx][0]
    
    def _get_labels_(self):
        return [self.fileList[idx][0] for idx in range(len(self.fileList))]
    
def cal_distribution(labels):
    length_count = defaultdict(lambda: 0)
    labels = sorted(labels)
    for l in labels:
        length_count[l] += 1
    
    length_group = defaultdict(lambda: 0)
    for x in length_count:
        length_group[length_count[x]] += 1
    
    X = np.arange(0, 1.0, 1.0/len(length_group))
    y = sorted(100*np.array([length_group[x] for x in sorted(length_group.keys())])/len(labels))
    return X, y
    
class TransformWrapper(Dataset):
    def __init__(self, dataset, transforms):
        self.dataset = dataset
        self.transforms = transforms
        
    def _get_image_(self, idx):
        image = self.dataset[idx][0]
        if self.transforms:
            return (self.transforms(image), *self.dataset[idx][1:])
        return (image, *self.dataset[idx][1:])
    
    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, idx):
        return self._get_image_(idx)
    
def get_labels(dataset, batch_size=default_batch_size, num_workers=default_num_workers):
    """
        Function Objective
        ------------------
        Get all dataset labels as numpy
        
        Non-defaut parameters
        ---------------------
        Dataset is MNIST dataset but can be either train or test
        
        Default parameters
        ------------------
        batch_size, and num_workers is used to define DataLoader instance
        verbose is used for output progress bar
        
        Returns
        -------
        Labels is a numpy array of size(len(dataset))
    """
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, shuffle=False)
    labels = np.zeros(len(dataloader.dataset))
    k = 0
    for _, target in dataloader:
        labels[k:k+len(target)] = target.numpy()
        k += len(target)
    return labels.astype(dtype=np.uint32)

def group_ids(labels):
    """
        Function Objective
        ------------------
        Group indexes of label by its label
        
        Non-default parameters
        ----------------------
        labels is a numpy labels from get_embeddings function
        
        Returns
        -------
        A defaultdict of groupped label indexes
    """
    datasetIdx = defaultdict(lambda: [])
    for idx, item in enumerate(labels):
        datasetIdx[item].append(idx)
        
    return datasetIdx

# Balanced Triplet Dataset length is batch_size * n_classes
# With each items is a tuple of (anchor, [positives], [negatives]), anchor_labels

class RandomTripletDataset(Dataset):
    def __init__(self, dataset, labels=None, transforms=None):
        super(RandomTripletDataset, self).__init__()
        self.dataset = dataset
        self.transforms = transforms
        if labels is None:
            labels = get_labels(self.dataset)
        self.label_to_idx = group_ids(labels)
        self.sample_size = len(self.label_to_idx.keys()) - 1 if self.dataset.train else 1
        
    def __len__(self):
        return len(self.dataset)*self.sample_size
    
    def __getitem__(self, idx):
        return self._match_random_(idx)
        
    def _get_image_(self, idx):
        image = self.dataset[idx][0]
        if self.transforms:
            return self.transforms(image)
        return image
    
    def _match_random_(self, index):
        idx = int(index//self.sample_size)
        
        label = int(self.dataset[idx][1])
        not_label = list(sorted(set(self.label_to_idx.keys()) - set([label])))
        
        if self.dataset.train:
            not_idx = not_label[int(idx%self.sample_size)]
            # Making sure that everything is selected
            return (
                self._get_image_(idx),
                self._get_image_(sample(self.label_to_idx[label], 1)[0]),
                self._get_image_(sample(self.label_to_idx[not_idx], 1)[0])
            ), label
        else:
            # Still random but just a positive and a negative sample
            return (
                self._get_image_(idx),
                self._get_image_(sample(self.label_to_idx[label], 1)[0]),
                self._get_image_(sample(self.label_to_idx[sample(list(not_label), 1)[0]], 1)[0])
            ), label