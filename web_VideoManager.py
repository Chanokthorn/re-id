import os

class VideoManager:
    def __init__(self):
        files = os.listdir("./HumanDetection/videos")
        self.videos = []
        for file in files:
            if file.endswith(".avi"):
                self.videos.append(file)
    def getVideosStatus(self):
        results = []
        #object = {embedded?, #identity, #frames}
        
        