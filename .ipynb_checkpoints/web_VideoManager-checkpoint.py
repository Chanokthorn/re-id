import os
import web_Clustering

class VideoManager:
    def __init__(self):
        files = os.listdir("./HumanDetection/videos")
        self.videos = []
        for file in files:
            if file.endswith(".avi") or file.endswith(".mp4"):
                self.videos.append(file)
        self.clusterings = {}
        for video in self.videos:
            self.clusterings[video] = web_Clustering.Clustering()
            self.clusterings[video].loadClustered(video)
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
                results.append(self.clusterings[video].getClusteringInfo())
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
        
        