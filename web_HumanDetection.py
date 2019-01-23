
# coding: utf-8

# In[10]:


import numpy as np
import tensorflow as tf
import cv2
import time
import sys
sys.path.insert(0, './HumanDetection')
from tensorflow_human_detection import DetectorAPI
import argparse
from network import embeddingNet
from web_api import Model
import matplotlib.pyplot as plt
import torch
import torchvision
import pickle
import os


# In[11]:


class HumanDetection:
    def __init__(self):
        self.videoDir = "HumanDetection/videos/"
        self.images = []
        return
    def detect(self, video="TownCentreXVID.avi", frameStep = 20, maxFrames = 300):
        threshold = 0.7
        images = []
        frameStepCounter = frameStep
        frameCounter = 0
        cap = cv2.VideoCapture(self.videoDir + video)
        while(cap.isOpened() and frameCounter <= maxFrames):
            ret, frame = cap.read()
            if frameStepCounter > 0:
                frameStepCounter -= 1
                continue
            frameStepCounter = frameStep
            frameCounter += 1
            if frame is None:
                break
            img = cv2.resize(frame, (1280, 720))
            boxes, scores, classes, num = self.odapi.processFrame(img)
            for i in range(len(boxes)):
                # Class 1 represents human
                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    images.append(img[box[0]:box[2], box[1]:box[3]])
        print("done loading: ", str(frameCounter), "frames")
        filePath = self.videoDir+video[:-4]+".p"
        cap.release()
        if os.path.exists(filePath):
            os.remove(filePath)
        pickle.dump(images, open( filePath, "wb" ))
        return
    def detectAllInImage(self, image):
        images = []
        threshold = 0.7
        img = cv2.resize(image, (1280, 720))
        boxes, scores, classes, num = self.odapi.processFrame(img)
        for i in range(len(boxes)):
            # Class 1 represents human
            if classes[i] == 1 and scores[i] > threshold:
                box = boxes[i]
                images.append(img[box[0]:box[2], box[1]:box[3]])
        self.images = images
        return images
    def getImage(self, index):
        return self.images[index]
    def loadModel(self):
        try:
            model_path = 'HumanDetection/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
            self.odapi = DetectorAPI(path_to_ckpt=model_path)
        except:
            pass
        return "success"
    def releaseModel(self):
        try:
            del self.odapi
        except:
            pass
        return "success"