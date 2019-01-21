import numpy as np
import pickle
import os
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
        self.video = video
        self.embeddings = pickle.load( open( self.videoDir + "embeddings-" + video[:-4]+".p", "rb" ) )
        return "done embedding"
    
    def loadClustered(self, video):
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
            return "clusters of " + video + " is loaded"
        else:
            return "not loaded: file does not exist"
    def projectEmbeddings(self, dim = 5):
        self.projectionDim = dim
        pca = PCA(n_components=self.projectionDim)
        pca.fit(self.embeddings)
        self.projectedEmbeddings = pca.transform(self.embeddings)
#         self.projectedEmbeddings = projectedEmbeddings
        return "done projecting"
    
    def dbscan(self, eps=3, min_samples=5):
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(self.embeddings)
        self.labels = clustering.labels_
        self.parameters = {"eps": eps, "min_samples": min_samples}
        return "done dbscan"
    
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
            return "done saving: " + filePath
        else:
            return "fail saving: " + filePath
    
    def plotClustering(self, video="TownCentreXVID.avi"):
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
        ax.scatter(embeddings[:, 0], embeddings[:, 1], embeddings[:, 2], c=labelColor, cmap=plt.cm.nipy_spectral,edgecolor='k')
        ax.w_xaxis.set_ticklabels([])
        ax.w_yaxis.set_ticklabels([])
        ax.w_zaxis.set_ticklabels([])
        filePath = self.videoDir + "plot-" + video[:-4]
        if os.path.exists(filePath + ".png"):
            os.remove(filePath + ".png")
        fig.savefig(filePath)
        self.plotResult = filePath + ".png"
        return "done"
    
    def getClusteringInfo(self):
        isSuccess = False
        try:
            result = {
                "embeddingAmount": self.embeddings.shape[0],
                "identityAmount": len(np.unique(self.labels)),
                "eps": self.parameters["eps"],
                "min_samples": self.parameters["min_samples"]
                }
            isSuccess = True
        except:
            isSuccess = False
        if isSuccess:
            return result
        else:
            print("failed getting info of the video")
            return None
    
    def getPlotResult(self):
        if self.plotResult == "":
            return None
        else:
            return self.plotResult