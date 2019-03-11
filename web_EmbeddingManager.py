import os
import pickle
import numpy as np
import collections

class EmbeddingManager:
    def __init__(self, videoDir="./HumanDetection/videos"):
        self.loadEmbeddings(videoDir = videoDir)
        return
    def loadEmbeddings(self, videoDir="./HumanDetection/videos"):
        self.videoDir = videoDir
        files = os.listdir(videoDir)
        self.videos = []
        self.embeddings = {}
        self.margin = 1
        for file in files:
            if file.endswith(".avi") or file.endswith(".mp4"):
                self.videos.append(file)
        for file in files:
            if file[:10] == "embedding-":
                videoName = file
                
        self.embeddings = {}
        self.margin = 1
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
        return "success"
    def setMargin(self, margin):
        self.margin = margin
        return "success"
    def calcDistance(self, em1, em2):
        subtraction = em1 - em2
        return np.dot(subtraction, subtraction)
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