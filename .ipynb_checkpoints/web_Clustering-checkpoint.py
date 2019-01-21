import numpy as np
import pickle
import os
import cv2
from sklearn.decomposition import PCA
import pandas as pd
from itertools import cycle
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from io import BytesIO
from mpl_toolkits.mplot3d import Axes3D

class Clustering:
    def __init__(self, videoDir="HumanDetection/videos/"):
        self.videoDir = videoDir
        self.projectionDim = 5
        self.plotResult = ''
        return
        
    def loadEmbeddings(self, video):
        isSuccess = False
        try:
            self.video = video
            self.embeddings = pickle.load( open( self.videoDir + "embeddings-" + video[:-4]+".p", "rb" ) )
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return "success"
        else:
            return "fail"
    
    def loadClustered(self, video):
        self.video = video
        fileClustered = None
        isSuccess = False
        try:
            fileClustered = pickle.load(open(self.videoDir + "clustered-" + video[:-4] + ".p", "rb"))
            self.loadEmbeddings(video)
            isSuccess = True
        except:
            fileClustered = None
            isSuccess = False
        if isSuccess:
            self.projectedEmbeddings = fileClustered['projectedEmbeddings']
            self.labels = fileClustered['labels']
            self.parameters = fileClustered['parameters']
            return "success"
        else:
            return "fail"
    def projectEmbeddings(self, dim = 5):
        isSuccess = False
        try:
            self.projectionDim = dim
            pca = PCA(n_components=self.projectionDim)
            pca.fit(self.embeddings)
            self.projectedEmbeddings = pca.transform(self.embeddings)
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return "success"
        else:
            return "fail"
    
    def dbscan(self, eps=3, min_samples=5):
        isSuccess = False
        try:
            clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(self.embeddings)
            self.labels = clustering.labels_
            self.parameters = {"eps": eps, "min_samples": min_samples}
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return "success"
        else:
            return "fail"
    
    def saveClustering(self):
        isSuccess = False
        try:
            result = {"projectedEmbeddings": self.projectedEmbeddings, "labels": self.labels,
                     "parameters": self.parameters}
            filePath = self.videoDir + "clustered-" + self.video[:-4] + ".p"
            if os.path.exists(filePath):
                 os.remove(filePath)
            pickle.dump( result, open(filePath, "wb"))
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return "success"
        else:
            return "fail"
    
    def plotClustering(self, video="TownCentreXVID.avi"):
        isSuccess = False
        try:
            plt.cla()
            embeddings = self.embeddings
            pca = PCA(n_components=3)
            pca.fit(embeddings)
            embeddings =  pca.transform(embeddings)
            labels = self.labels.tolist()
            cycol = cycle('bgrcmk')
            colors = []
            for i in range(np.unique(self.labels).shape[0]):
                colors.append(next(cycol))
            labelColor = []
            for label in labels:
                labelColor.append(colors[label-1])
            print(labelColor)

            fig = plt.figure(1, figsize=(10, 10))
            ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
            ax.scatter(embeddings[:, 0], embeddings[:, 1], embeddings[:, 2], 
                       c=labelColor, cmap=plt.cm.nipy_spectral,edgecolor='k')
            ax.w_xaxis.set_ticklabels([])
            ax.w_yaxis.set_ticklabels([])
            ax.w_zaxis.set_ticklabels([])
            filePath = self.videoDir + "plot-" + video[:-4]
            if os.path.exists(filePath + ".png"):
                os.remove(filePath + ".png")
            fig.savefig(filePath)
            self.plotResult = cv2.imread(filePath + ".png")
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return "success"
        else:
            return "fail"
    
    def getClusteringInfo(self):
        isSuccess = False
        try:
            result = {
                "video": self.video,
                "status": "clustered",
                "embeddingAmount": self.embeddings.shape[0],
                "identityAmount": len(np.unique(self.labels)),
                "eps": self.parameters["eps"],
                "min_samples": self.parameters["min_samples"]
                }
            isSuccess = True
        except:
            try:
                loadResult = this.loadEmbeddings(self.video)
                if loadResult == "success":
                    result = {
                        "video": self.video,
                        "status": "embeddingOnly",
                        "embeddingAmount": self.embeddings.shape[0],
                    }
                    isSuccess = True
                else:
                    isSuccess = False
            except:
                isSuccess = False
        if not isSuccess:
            result = {
                "video": self.video,
                "status": "noEmbedding"
            }
        return result
    
    def getPlotResult(self):
        fileDir = self.videoDir + "plot-" + self.video[:-4] + ".png"
        if os.path.exists(fileDir):
            self.plotResult = cv2.imread(fileDir)
            return self.plotResult
        else:
            return "fail"