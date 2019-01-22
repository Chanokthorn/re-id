from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from flask_cors import CORS, cross_origin
import json
import os
import web_HumanDetection
import web_ImageListEmbedder
import web_Clustering
import web_DisplayImage
import web_Pyrebase
import web_VideoManager
from flask import send_file
import cv2

# humanDetection = web_HumanDetection.HumanDetection()
imageListEmbedder = web_ImageListEmbedder.ImageListEmbedder()
# clustering = web_Clustering.Clustering()
displayImage = web_DisplayImage.DisplayImage()
videoManager = web_VideoManager.VideoManager()


img_static = "img_Static"
img_detectedPerson = "img_DetectedPerson"
img_plotResults = "img_PlotResults"

app = Flask(__name__)
CORS(app)

@app.route("/")
def initialize():
    return "loaded"

@app.route('/detect',methods=['GET','POST'])
def detect():
    video = request.args.get('video')
    frameStep = request.args.get('frameStep')
    maxFrames = request.args.get('maxFrames')
    humanDetection = web_HumanDetection.HumanDetection()
    print("detecting...")
    humanDetection.detect(video = video, frameStep = int(frameStep), maxFrames = int(maxFrames))

#     try:
#         humanDetection.detect(video = video, frameStep = int(frameStep), maxFrames = int(maxFrames))
#     except:
#         pass
    del humanDetection
    print("done")
    return 'ok'



@app.route('/embed', methods=['GET','POST'])
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

@app.route('/projectEmbedding', methods=['POST'])
def projectEmbedding():
    video = request.form['video']
    projectionDim = request.form['projectionDim']
    clustering.loadEmbeddings(video)
    clustering.projectEmbeddings(int(projectionDim))
    return "done projecting embeddings"

@app.route('/cluster', methods=['GET','POST'])
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

@app.route('/plot', methods=['GET','POST'])
def plot():
    video = request.args.get('video')
    plotResult = videoManager.getPlotResult(video)
    if plotResult == "fail":
        return "fail"
    else:
        return jsonify(url=displayImage.createImage(plotResult, "img_PlotResults"))

# @app.route('/plot')
# def plot():
#     clustering.plotClustering()
#     plotResult = clustering.getPlotResult()
#     return send_file(plotResult, mimetype='image/png')

@app.route("/display", methods=['POST'])
def display():
    imgPath = "../Market-1501-v15.09.15/bounding_box_train/0326_c6s4_007552_02.jpg"
    img = cv2.imread(imgPath)
    return displayImage.display(img)

@app.route("/detectInImage", methods=['POST'])
def detectInImage():
    img = cv2.imread("humans.png")
    images = humanDetection.detectAllInImage(img)
    urls = []
    for image in images:
        url = displayImage.createImage(image, img_detectedPerson)
        urls.append(url)
    return jsonify(urls=urls)
    
@app.route("/clear", methods=['POST'])
def clear():
    folder = request.form['folder']
    result = displayImage.clear(folder)
    return result

@app.route("/clearAll", methods=['POST'])
def clearAll():
    result = displayImage.clearAll()
    return result

@app.route("/checkVideoStatus")
def checkVideoStatus():
    video = request.args.get('video')
    result = videoManager.getVideoStatus(video)
    return jsonify(result = result)
@app.route("/checkVideosStatus")
def checkVideosStatus():
    results = videoManager.getVideosStatus()
    if results == "fail":
        return results
    else:
        return jsonify(results = results)
    
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", debug=True)
