from flask import Flask, render_template, jsonify, request, redirect, url_for, Response, send_from_directory
from flask_cors import CORS, cross_origin
import json
import os
import web_HumanDetection
import web_ImageListEmbedder
import web_Clustering
import web_ClusteringManager
import web_DisplayImage
import web_Pyrebase
import web_VideoManager
import web_VideoHandler
from flask import send_file
import cv2

humanDetection = web_HumanDetection.HumanDetection()
humanDetection.loadModel()
imageListEmbedder = web_ImageListEmbedder.ImageListEmbedder()
# imageListEmbedder.loadModel()
# clustering = web_Clustering.Clustering()
displayImage = web_DisplayImage.DisplayImage()
videoManager = web_VideoManager.VideoManager()

videoManager.setInitTimeStub()

videoHandler = web_VideoHandler.VideoHandler()
clusteringManager = web_ClusteringManager.ClusteringManager()

# clusteringManager.setInitTimeStub()

img_static = "img_Static"
img_detectedPerson = "img_DetectedPerson"
img_plotResults = "img_PlotResults"
img_Frames = "img_Frames"
UPLOAD_FOLDER = './img_temp'
BASE_URI = "/thananop/ssdfaces"

app = Flask(__name__)
CORS(app)

@app.route(BASE_URI + "/")
def initialize():
    return "loaded"

@app.route(BASE_URI + "/imageStorage/<path:path>", methods=['GET'])
def serve_image(path):
    print(UPLOAD_FOLDER,path)
    if not os.path.isfile(os.path.join(UPLOAD_FOLDER,path)):
        return "<center><b>403 Forbidden</b></center>"
    print("served")
    return send_from_directory(UPLOAD_FOLDER, path)

@app.route(BASE_URI + '/detect',methods=['GET','POST'])
def detect():
    video = request.args.get('video')
    frameStep = request.args.get('frameStep')
    maxFrames = request.args.get('maxFrames')
    
    print("detecting...")
    humanDetection.detect(video = video, frameStep = int(frameStep), maxFrames = int(maxFrames))

#     try:
#         humanDetection.detect(video = video, frameStep = int(frameStep), maxFrames = int(maxFrames))
#     except:
#         pass
    print("done")
    return 'ok'



@app.route(BASE_URI + '/embed', methods=['GET','POST'])
def embed():
    video = request.args.get('video')
    imageListEmbedder.embed(video = video)
#     imageListEmbedder = web_ImageListEmbedder.ImageListEmbedder()
#     try:
#         video = request.args.get('video')
#         imageListEmbedder.embed(video = video)
#     except:
#         pass
#     del imageListEmbedder
    return "done embedding"

@app.route(BASE_URI + '/projectEmbedding', methods=['POST'])
def projectEmbedding():
    video = request.form['video']
    projectionDim = request.form['projectionDim']
    clustering.loadEmbeddings(video)
    clustering.projectEmbeddings(int(projectionDim))
    return "done projecting embeddings"

@app.route(BASE_URI + '/cluster', methods=['GET','POST'])
def cluster():
    video = request.args.get('video')
    eps = request.args.get('eps')
    min_samples = request.args.get('min_samples')
    projectionDim = request.args.get('projectionDim')
    clustering = web_Clustering.Clustering()
    print("start")
    print("process")
    videoManager.cluster(video, float(eps), int(min_samples), int(projectionDim))
    del clustering
#     try:
#         print("process")
#         clustering.loadEmbeddings(video)
#         clustering.projectEmbeddings(int(dim))
#         clustering.dbscan(eps=0.5, min_samples=7)
#         print("done")
#     except:
#         print("fail")
#         pass
    return "done clustering"

@app.route(BASE_URI + '/plot', methods=['GET','POST'])
def plot():
    video = request.args.get('video')
    plotResult = videoManager.getPlotResult(video)
    if plotResult == "fail":
        return "fail"
    else:
#         return jsonify(url=displayImage.createImage(plotResult, "img_PlotResults"))
        return jsonify(url=displayImage.createImageLocal(plotResult))

# @app.route('/plot')
# def plot():
#     clustering.plotClustering()
#     plotResult = clustering.getPlotResult()
#     return send_file(plotResult, mimetype='image/png')

@app.route(BASE_URI + "/display", methods=['POST'])
def display():
    imgPath = "../Market-1501-v15.09.15/bounding_box_train/0326_c6s4_007552_02.jpg"
    img = cv2.imread(imgPath)
    return displayImage.display(img)

@app.route(BASE_URI + "/detectInImage", methods=['POST'])
def detectInImage():
    img = cv2.imread("humans.png")
#     humanDetection.loadModel()
    images = humanDetection.detectAllInImage(img)
    urls = []
    for image in images:
        url = displayImage.createImageLocal(image, img_detectedPerson)
        urls.append(url)
    return jsonify(urls=urls)
    
@app.route(BASE_URI + "/clear", methods=['POST'])
def clear():
    folder = request.form['folder']
    result = displayImage.clear(folder)
    return result

@app.route(BASE_URI + "/clearAll", methods=['POST'])
def clearAll():
    result = displayImage.clearAll()
    return result

@app.route(BASE_URI + "/clearLocal", methods=['GET', 'POST'])
def clearLocal():
    result = displayImage.clearLocal()
    return result


@app.route(BASE_URI + "/checkVideoStatus")
def checkVideoStatus():
    video = request.args.get('video')
    result = videoManager.getVideoStatus(video)
    return jsonify(result = result)
# @app.route(pton + "/checkVideosStatus")

@app.route(BASE_URI + "/checkVideosStatus")
def checkVideosStatus():
    results = videoManager.getVideosStatus()
    if results == "fail":
        return results
    else:
        return jsonify(results = results)
    
@app.route(BASE_URI + '/loadVideo', methods=['GET','POST'])
def loadVideo():
    video = request.args.get('video')
    result = videoHandler.loadVideo(video)
    return jsonify(result = result)

@app.route(BASE_URI + '/setFrameStep', methods=['GET','POST'])
def setFrameStep():
    frameStep = request.args.get('frameStep')
    result = videoHandler.setFrameStep(int(frameStep))
    return jsonify(result = result)

@app.route(BASE_URI + '/getFrame', methods=['GET','POST'])
def getFrame():
    image = videoHandler.getFrame()
#     return jsonify(url=displayImage.createImage(image, img_Frames))
    return jsonify(url=displayImage.createImageLocal(image))

@app.route(BASE_URI + '/getNextFrame', methods=['GET','POST'])
def getNextFrame():
    image = videoHandler.getNextFrame()
#     return jsonify(url=displayImage.createImage(image, img_Frames))
    return jsonify(url=displayImage.createImageLocal(image))

@app.route(BASE_URI + '/getPrevFrame', methods=['GET','POST'])
def getPrevFrame():
    image = videoHandler.getPrevFrame()
#     return jsonify(url=displayImage.createImage(image, img_Frames))
    return jsonify(url=displayImage.createImageLocal(image))

@app.route(BASE_URI + '/getFrameIndex', methods=['GET','POST'])
def getFrameIndex():
    index = request.args.get('index')
    print("begin")
    image = videoHandler.getFrameIndex(index)
    print("end")
    return jsonify(url=displayImage.createImageLocal(image))

@app.route(BASE_URI + "/detectFrame", methods=['GET','POST'])
def detectFrame():
    img = videoHandler.getFrame()
    images = humanDetection.detectAllInImage(img)
    results = []
    for index in range(len(images)):
        image = images[index]
        result = displayImage.createImageLocal(image)
        results.append(result)
    return jsonify(results=results)

@app.route(BASE_URI + "/setMargin", methods=['GET','POST'])
def setMargin():
    margin = request.args.get('margin')
    result = clusteringManager.setMargin(margin)
    return result
    

@app.route(BASE_URI + "/findPerson", methods=['GET','POST'])
def findPerson():
    url = request.args.get('url')
    mode = request.args.get('mode')
    image = humanDetection.getImage(url)
    embedding = imageListEmbedder.embedImage(image)
    if mode == "useCluster":
        result = clusteringManager.find(embedding)
    else:
        result = clusteringManager.findFull(embedding)
    return jsonify(result=result)

@app.route(BASE_URI + "/findPersonWithFrame", methods=['GET','POST'])
def findPersonWithFrame():
    url = request.args.get('url')
    mode = request.args.get('mode')
    image = humanDetection.getImage(url)
    embedding = imageListEmbedder.embedImage(image)
    if mode == "useCluster":
        result = clusteringManager.find(embedding)
    else:
        result = clusteringManager.findFullWithFrame(embedding)
    return jsonify(result=result)
    
@app.route(BASE_URI + "/observe", methods=['GET','POST'])
def observe ():
    video = request.args.get('video')
    result = clusteringManager.observe(video)
    return jsonify(result=result)

@app.route(BASE_URI + "/getFrameOfVideo", methods=['GET','POST'])
def getFrameOfVideo():
    videoName = request.args.get('videoName')
    frameIndex = request.args.get('frameIndex')
    image = videoHandler.getFrameOfVideo(videoName,frameIndex)
    return jsonify(url=displayImage.createImageLocal(image))

from random import randint
@app.route(BASE_URI + '/stressTest', methods=['GET','POST'])
def stressTest():
    index = request.args.get('max')
    for i in range(100):
#         index = randint(0, int(index)-3)
        index = randint(0,300)
        image = videoHandler.getFrameIndex(index)
        print('success')
    return 
    

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", debug=True, threaded=False)
# if __name__ == '__main__':
#     app.run()