
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
        self.localFolder = "img_temp/"
        self.loadModel()
        return
    def detect(self, video="TownCentreXVID.avi", frameStep = 20, maxFrames = 300):
        threshold = 0.7
        images = []
        frameStepCounter = frameStep
        frameCounter = 0
        frameIndices = []
        frameIndex = 0
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
            img = cv2.resize(frame, (300, 300))
            boxes, scores, classes, num = self.odapi.processFrame(img)
            for i in range(len(boxes)):
                # Class 1 represents human
                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    images.append(img[box[0]:box[2], box[1]:box[3]])
                    frameIndices.append(frameIndex)
            frameIndex += frameStep
        print("done loading: ", str(frameCounter), "frames")
        filePath = self.videoDir+video[:-4]+".p"
        cap.release()
        if os.path.exists(filePath):
            os.remove(filePath)
        pickle.dump([images,frameIndices], open( filePath, "wb" ))
        return
    def detectAllInImage(self, image):
        images = []
        threshold = 0.7
        img = cv2.resize(image, (640, 640))
        boxes, scores, classes, num = self.odapi.processFrame(img)
        for i in range(len(boxes)):
            # Class 1 represents human
            if classes[i] == 1 and scores[i] > threshold:
                box = boxes[i]
                images.append(img[box[0]:box[2], box[1]:box[3]])
        self.images = images
        return images
    def getImage(self, fileName):
        file = self.localFolder + fileName
        image = cv2.imread(file)
        return image
    def loadModel(self):
        model_path = './HumanDetection/faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
#         try:
#             model_path = 'ssd_mobilenet_v1_0.75_depth_300x300_coco14_sync_2018_07_03/frozen_inference_graph.pb'
#             self.odapi = DetectorAPI(path_to_ckpt=model_path)
#         except:
#             pass
#         model_path = '/home/bone/ssd_mobilenet_v1_0.75_depth_300x300_coco14_sync_2018_07_03/frozen_inference_graph.pb'
#         model_path = '/home/bone/share/CV/Official_ReID/ssd_mobilenet_v1_fpn_shared_box_predictor_640x640_coco14_sync_2018_07_03/frozen_inference_graph.pb'
        self.odapi = DetectorAPI(path_to_ckpt=model_path)
        return "success"
    def releaseModel(self):
        try:
            del self.odapi
        except:
            pass
        return "success"