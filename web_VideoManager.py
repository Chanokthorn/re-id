import os
import web_Clustering
from tqdm import tqdm, tqdm_notebook
import cv2
import numpy as np
import time
import random

class VideoManager:
    def __init__(self):
        files = os.listdir("./HumanDetection/videos")
        self.videoDir = "./HumanDetection/videos/"
        self.videos = []
        
        self.videosInitTime = {}
        self.videosLength = {}
        
        for file in files:
#             if file.endswith(".avi") or file.endswith(".mp4"):
            if file.endswith(".avi") or file.endswith(".mp4"):
                self.videos.append(file)
        self.clusterings = {}
        for video in self.videos:
            self.clusterings[video] = web_Clustering.Clustering()
            cap = cv2.VideoCapture(self.videoDir + video)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.videosLength[video] = length
            self.clusterings[video].loadClustered(video)
            
    def setInitTimeStub(self):
        for video in self.videos:
            margin = 15
            params = random.randint((-1 * margin), margin)
            self.videosInitTime[video] = int(time.time() + params)
            print("DONE: ", self.videosInitTime[video])
    
    def storeVideo(self, video):
        cap = cv2.VideoCapture(self.videoDir + video)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = 480
        height = 320
        videoArray = np.ndarray((length, height, width))
        for i in tqdm(range(length)):
            if cap.isOpened():
                _, frame = cap.read()
                if frame is None:
                    break
                frame = cv2.resize(frame, (width, height))
                videoArray[i,:] = frame
        cap.release()
        outputDir = self.videoDir + "array-" + video[:-4] + ".npy"
        np.save(outputDir, videoArray)
        return "success"
            
    def cluster(self, video, eps, min_samples, projectionDim):
        self.clusterings[video].projectEmbeddings(int(projectionDim))
        self.clusterings[video].dbscan(eps=float(eps), min_samples=int(min_samples))
        self.clusterings[video].saveClustering()
        self.clusterings[video].plotClustering()
        return "success"
    def getVideoStatus(self, video):
        isSuccess = False
        try:
            result = self.clusterings[video].getClusteringInfo()
            isSuccess = True
        except:
            pass
        if isSuccess:
            return result
        else:
            return "fail"
    def getVideosStatus(self):
        isSuccess = False
        try:
            results = []
            for video in self.videos:
#                 self.clusterings[video].loadClustered(video)
                result = self.clusterings[video].getClusteringInfo()
                result["initTime"] = self.videosInitTime[video]
                result["videoLength"] = self.videosLength[video]
                results.append(result)
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return results
        else:
            return "fail"
    def getPlotResult(self, video):
        isSuccess = False
        result = ""
        try:
            result = self.clusterings[video].getPlotResult()
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return result
        else:
            return "fail"
        
        