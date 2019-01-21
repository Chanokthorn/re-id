from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from flask_cors import CORS, cross_origin
import json
import os
import web_HumanDetection
import web_ImageListEmbedder
import web_Clustering
import web_DisplayImage
import web_Pyrebase
from flask import send_file
import cv2

humanDetection = web_HumanDetection.HumanDetection()
# imageListEmbedder = web_ImageListEmbedder.ImageListEmbedder()
# clustering = web_Clustering.Clustering()
displayImage = web_DisplayImage.DisplayImage()

static = "img_Static"
detectedPerson = "img_DetectedPerson"
plotResults = "img_PlotResults"

app = Flask(__name__)
CORS(app)

@app.route("/")
def initialize():
    return "loaded"

@app.route('/detect',methods=['POST'])
def detect():
    video = request.form['video']
    frameStep = request.form['frameStep']
    maxFrames = request.form['maxFrames']
    print("detecting...")
    humanDetection.detect(video = video, frameStep = int(frameStep), maxFrames = int(maxFrames))
    print("done")
    return 'ok'

@app.route('/embed', methods=['POST'])
def embed():
    video = request.form['video']
    imageListEmbedder.embed(video = video)
    return "done embedding"

@app.route('/projectEmbedding', methods=['POST'])
def projectEmbedding():
    video = request.form['video']
    dim = request.form['dim']
    clustering.loadEmbeddings(video)
    clustering.projectEmbeddings(int(dim))
    return "done projecting embeddings"

@app.route('/cluster', methods=['POST'])
def cluster():
    eps = request.form['eps']
    min_samples = request.form['min_samples']
    clustering.dbscan(eps=0.5, min_samples=7)
    return "done clustering"

@app.route('/plot')
def plot():
    clustering.plotClustering()
    plotResult = clustering.getPlotResult()
    return send_file(plotResult, mimetype='image/png')

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
        url,index = displayImage.createImage(image, detectedPerson)
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
def checkVideosStatus():
    
    
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host="0.0.0.0", debug=True)
