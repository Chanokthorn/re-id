
# coding: utf-8

# In[144]:


import numpy as np
import tensorflow as tf
import cv2
import time
import sys
sys.path.insert(0, './HumanDetection')
from tensorflow_human_detection import DetectorAPI
from tqdm import tqdm, tqdm_notebook
import argparse
from network import embeddingNet
from web_api import Model
import matplotlib.pyplot as plt
import torch
import torchvision
import pickle
import os


# In[196]:


class ImageListEmbedder:
    def __init__(self, videoDir="HumanDetection/videos/"):
        self.videoDir = videoDir
        self.model = Model()
        return
    def embed(self, video="TownCentreXVID.avi", threshold = 1):
        self.images = pickle.load( open( self.videoDir+video[:-4]+".p", "rb" ) )
        embeddings = []
        
        for i in tqdm(range(len(self.images))):
            image = self.images[i]
            embedding = self.model.forward(image)
            embeddings.append(embedding)
        embeddings = np.asarray(embeddings)
        embeddings = np.squeeze(np.transpose(embeddings, (0,2,1)), axis=2)
        filePath = self.videoDir + "embeddings-" + video[:-4]+".p"
        if os.path.exists(filePath):
            os.remove(filePath)
        pickle.dump( embeddings, open(filePath, "wb"))
        return "done"

#         embeddingDict = {} # (identity, list of embeddings)
#         personDict = {} # (identity, representative embedding)
#         imageDict = {}
#         personCounter = 0
#         threshold = 1

#         labels = []

#         for i in tqdm(range(len(embeddings))):
#             embedding = embeddings[i]
#             foundMatch = False
#             for key in personDict:
#                 representative = np.asarray(embeddingDict[key])
#                 representative = np.average(representative, axis=0)
#                 dist = np.linalg.norm(embedding-representative)
#                 if dist <= threshold:
#                     embeddingDict[key].append(embedding)
#                     personDict[key] = representative
#                     imageDict[key].append(self.images[i])
#                     foundMatch = True

#                     labels.append(key)

#                     break
#             if not foundMatch:
#                 personCounter += 1
#                 embeddingDict[personCounter] = [embedding]
#                 personDict[personCounter] = embedding
#                 imageDict[personCounter] = [image]

#                 labels.append(personCounter)
#         pickle.dump( personDict, open(self.videoDir + "processed-" + video[:-4]+".p", "wb" ) )
#         return 'ok'
        

