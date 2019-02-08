import numpy as np
import cv2
import os
from flask import url_for
# import web_Pyrebase
import random
import string


class DisplayImage:
    
    def __init__(self):
        self.storeIndex = {
            "img_Static": 0,
            "img_PlotResults": 0,
            "img_DetectedPerson": 0,
            "img_Frames": 0,
            "img_temp": 0
        }
        self.localFileTrackerSize = 20
        self.localFileTracker = []
#         self.pyrebase = web_Pyrebase.Pyrebase()
        self.localFolder = "img_temp"
        return
    
    def createImage(self, input, folder, indexing=False, index=None):
        fileDir = folder + "/" + str(self.storeIndex[folder]) + ".png"
        cv2.imwrite(fileDir, input)
        self.storeIndex[folder] += 1
        url, counter = self.pyrebase.storeFile(fileDir, folder)
        if indexing:
            return {"url": url, "index": index}
        return url
    
    def clear(self, folder):
        if self.storeIndex[folder] == 0: 
            return "done clearing " + folder
        for i in range(self.storeIndex[folder]):
            os.remove(folder + "/" + str(i) + ".png")
        self.storeIndex[folder] = 0
        self.pyrebase.clear(folder)
        return "done clearing " + folder
    
    def clearAll(self):
        for folder in  self.storeIndex:
            self.clear(folder)
#             if self.storeIndex[folderName] == 0: pass
#             for i in range(self.storeIndex[folderName]):
#                 os.remove(folderName + "/" + str(i) + ".png")
        self.pyrebase.clearAll()
        return "done clearing locally"
    
    def createFileLocal(self, input):
        fileId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        fileName = fileId + ".png"
        fileDir = self.localFolder + "/" + fileName
        if os.path.exists(fileDir):
            os.remove(fileDir)
        cv2.imwrite(fileDir, input)
        self.storeIndex["img_temp"] += 1
        self.localFileTracker.append(fileDir)
        print("fileTrackerSize: " +  str(len(self.localFileTracker)))
        return fileName
    
    def createImageLocal(self, input):
        if len(self.localFileTracker) > self.localFileTrackerSize:
            os.remove(self.localFileTracker[0])
            del self.localFileTracker[0]
        fileName = self.createFileLocal(input)
        return fileName
    
    def createImageLocalWithIndex(self, input, index=None):
        if len(self.localFileTracker) > self.localFileTrackerSize:
            os.remove(self.localFileTracker[0])
            del self.localFileTracker[0]
        fileName = str( self.storeIndex["img_temp"]) + ".png"
        fileDir = self.localFolder + "/" + fileName
        cv2.imwrite(fileDir, input)
        self.storeIndex["img_temp"] += 1
        return {"url": fileName, "index": index}
    
    def clearLocal(self):
        folder = "img_temp"
        files = os.listdir(folder)
        images = []
        self.storeIndex[folder] = 0
        for file in files:
            if file.endswith(".png") or file.endswith(".jpeg"):
                images.append(file)
        if len(images) == 0: 
            return "done clearing " + folder
        for image in images:
            os.remove(folder + "/" + image)
        return "done clearing " + folder
        