import cv2
import matplotlib.pyplot as plt

# class VideoHandler:
#     def __init__(self, videoDir="HumanDetection/videos/"):
#         self.video = ""
#         self.videoDir = videoDir
#         self.index = 0
#         self.frames = []
#         self.frameStep = 10
#         return
#     def loadVideo(self, video):
#         self.index = 0
#         self.video = video
#         del self.frames
#         self.frames = []
#         cap = cv2.VideoCapture(self.videoDir + video)
#         length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         frameAmount = length // self.frameStep

#         frameStepCounter = self.frameStep
#         while cap.isOpened():
#             _, frame = cap.read()
#             if frameStepCounter > 0:
#                 frameStepCounter -= 1
#                 continue
#             frameStepCounter = self.frameStep
#             if frame is None:
#                 break
                
#             frame = cv2.resize(frame, (1280, 720))
#             self.frames.append(frame)
#             print("\r frame: " + str(len(self.frames)))
#         cap.release()
#         return "success"
#     def setFrameStep(self, frameStep):
#         self.frameStep = frameStep
#         return "success"
#     def getFrame(self):
#         frame = self.frames[self.index]
#         frame = cv2.resize(frame, (480, 320))
#         return frame
#     def getNextFrame(self):
#         if self.index + 1 <= len(self.frames) - 1:
#             self.index += 1
#         return self.getFrame()
#     def getPrevFrame(self):
#         if self.index - 1 >= 0:
#             self.index -= 1
#         return self.getFrame()
#     def releaseFrames(self):
#         self.frames = []
#         self.index = 0
#         return "success"

class VideoHandler:
    def __init__(self, videoDir="HumanDetection/videos/"):
        self.video = ""
        self.videoDir = videoDir
        self.index = 0
        self.frames = []
        self.frameStep = 10
        return
    def loadVideo(self, video):
        self.index = 0
        self.video = video
        del self.frames
        self.frames = []
        self.cap = cv2.VideoCapture(self.videoDir + video)
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        return self.length
    def setFrameStep(self, frameStep):
        self.frameStep = frameStep
        return "success"
    def getFrameIndex(self, index):
        index = int(index)
        if index in range(self.length):
            self.cap.set(1,index)
            _, frame = self.cap.read()
            self.currentFrame = frame
            frame = cv2.resize(frame, (480, 320))
            return (frame)
        else: return
    def getFrame(self):
        return self.currentFrame
#     def getFrame(self):
#         frame = self.frames[self.index]
#         frame = cv2.resize(frame, (480, 320))
#         return frame
    def getNextFrame(self):
        if self.index + 1 <= len(self.frames) - 1:
            self.index += 1
        return self.getFrame()
    def getPrevFrame(self):
        if self.index - 1 >= 0:
            self.index -= 1
        return self.getFrame()
    def releaseFrames(self):
        self.frames = []
        self.index = 0
        return "success"