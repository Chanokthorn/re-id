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

videoHandler = web_VideoHandler.VideoHandler()
UPLOAD_FOLDER = './img_temp'
BASE_URI = "/thananop/ssdfaces"
result = videoHandler.loadVideo(video)

app = Flask(__name__)
CORS(app)

@app@app.route(BASE_URI + "/")
def initialize():
    return "loaded"