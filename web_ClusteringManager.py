import os
import pickle
import numpy as np
import random
import web_DisplayImage
import time
import cv2

class ClusteringManager:
    def __init__(self, videoDir="./HumanDetection/videos"):
        self.margin = 1
        self.maxOutput = 10
        self.loadClusters(videoDir = videoDir)
        self.displayImage = web_DisplayImage.DisplayImage()
        return
    def loadClusters(self, videoDir="./HumanDetection/videos"):
        self.videoDir = videoDir
        files = os.listdir(videoDir)
        self.foundIndices = {}
        self.videos = []
        self.vidsReps = {}
        self.vidInitTime = {}
        self.vidsLength = {}
        self.vidsEms = {}
        self.margin = 0.3
        for file in files:
            if file.endswith(".avi") or file.endswith(".mp4"):
                self.videos.append(file)
        for video in self.videos:
            repPath = self.videoDir + "/" + "representative-" + video[:-4] + ".p"
            print("finding: ", repPath)
            fileExist = False
            try:
                rep = pickle.load( open(repPath, "rb" ) )
                fileExist = True
            except:
                fileExist = False
            if fileExist:
                self.vidsReps[video] = rep
                
            emPath = self.videoDir + "/" + "embeddings-" + video[:-4] + ".p"
            print("finding: ", emPath)
            fileExist = False
            try:
                [em, frameIndices] = pickle.load( open(emPath, "rb" ) )
                fileExist = True
            except:
                fileExist = False
            if fileExist:
                self.vidsEms[video] = {"em": em, "frameIndices": frameIndices}
                cap = cv2.VideoCapture("video.mp4")
                length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.release()
                self.vidsLength[video] = length
        return "success"
    
#     def setInitTimeStub(self):
#         for video in self.videos:
#             margin = 15
#             params = random.randint((-1 * margin), margin)
#             self.vidInitTime[video] = int(time.time() + params)
#             print("DONE: ", self.vidInitTime[video])
        return "success"
    def setMargin(self, margin):
        self.margin = float(margin)
        return "success"
    def calcDistance(self, em1, em2):
        subtraction = em1 - em2
        return np.dot(subtraction, subtraction)
    def calcDistanceVectorized(self, inputEm, ems):
        distances = inputEm - ems
        distances = np.sum(distances * distances, axis=-1)
        return distances
    def findFull(self, inputEm):
        imageInVids = {}
        results = []
        self.foundIndices = {}
        for vid in self.vidsEms:
            distances = self.calcDistanceVectorized(inputEm, self.vidsEms[vid]["em"])
#             print(distances)
            foundIndices = np.where(distances < self.margin)
#             print(foundIndices)
            if foundIndices[0].shape[0] > 0:
                results.append({"videoName":vid})
                self.foundIndices[vid] = foundIndices[0].tolist()
        return results
    def setInitialTime(self, videoName, time):
        self.vidInitTime[videoName] = time
        return "set time success"
    def findFullWithFrame(self, inputEm):
        imageInVids = {}
        results = []
        self.foundIndices = {}
        for vid in self.vidsEms:
            distances = self.calcDistanceVectorized(inputEm, self.vidsEms[vid]["em"])
#             print(distances)
            foundIndices = np.where(distances < self.margin)
            foundFrameIndices = np.take(self.vidsEms[vid]["frameIndices"], foundIndices[0]).tolist()
#             print(foundIndices)
            if foundIndices[0].shape[0] > 0:
                results.append({"videoName":vid,"frameIndices":foundFrameIndices})
                self.foundIndices[vid] = foundIndices[0].tolist()
#                 self.foundFrameIndices[vid] = foundFrameIndices
        return results
            
    def find(self, em):
        results = []
        for vid in self.vidsReps:
            found = False
            for index in self.vidsReps[vid]:
                rep = self.vidsReps[vid][index]
                distance = self.calcDistance(em, rep)
                if distance <= self.margin:
                    found = True
                    break
            if found:
                results.append(vid)
        return results
    
    def getFoundImages(self):
        result = {}
        for vid in self.foundIndices:
            fileDir = self.videoDir+ "/" +vid[:-4]+".p"
            print("loading images from: ", fileDir)
            images = pickle.load( open(fileDir , "rb" ) )
            indices = self.foundIndices[vid]
#             print("indices", indices)
            result[vid] = []
            if len(indices) > self.maxOutput:
                for i in range(self.maxOutput):
                    randIndex = random.choice(indices)
                    url=self.displayImage.createImageLocal(images[randIndex])
                    result[vid].append(url)
            else:
                for i in range(len(indices)):
                    index = indices[i]
                    url=self.displayImage.createImageLocal(images[index])
                    result[vid].append(url)
        return result
    def observe(self, vid):
        result = []
        fileDir = self.videoDir+ "/" +vid[:-4]+".p"
        print("loading images from: ", fileDir)
        [images, foundFrameIndices] = pickle.load( open(fileDir , "rb" ) )
        indices = self.foundIndices[vid]
        if len(indices) > self.maxOutput:
            for i in range(self.maxOutput):
                randIndex = random.choice(indices)
                print("VID: {}, FRAME: {}".format(vid, foundFrameIndices[randIndex]))
                url=self.displayImage.createImageLocal(images[randIndex])
                result.append(url)
        else:
            for i in range(len(indices)):
                index = indices[i]
                url=self.displayImage.createImageLocal(images[index])
                print("VID: {}, FRAME: {}".format(vid, foundFrameIndices[index]))
                result.append(url)
        return result