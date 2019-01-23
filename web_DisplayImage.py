import numpy as np
import cv2
import os
from flask import url_for
import web_Pyrebase


class DisplayImage:
    def __init__(self):
        self.storeIndex = {
            "img_Static": 0,
            "img_PlotResults": 0,
            "img_DetectedPerson": 0,
            "img_Frames": 0
        }
        self.pyrebase = web_Pyrebase.Pyrebase()
        return
    def createImage(self, input, folder):
        fileDir = folder + "/" + str(self.storeIndex[folder]) + ".png"
        cv2.imwrite(fileDir, input)
        self.storeIndex[folder] += 1
        url, index = self.pyrebase.storeFile(fileDir, folder)
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