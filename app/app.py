import cv2
import os
import sys
# Get the current file path and add it to the python sys path (allows us to use our object_detectin module independent of the current working directory)
sys.path.insert(0, os.path.dirname(__file__))
from object_detection import Detector

from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__, template_folder='templates')
detector = Detector()
cap = cv2.VideoCapture(0)

@app.route("/")
def index():
    return render_template('/index.html')


@app.route("/videos", methods=['POST'])
def video():
    if request.method == 'POST':
        ret, pre_detection_img = cap.read()
        img, object_info, stroke_data = detector.detect_object(pre_detection_img)
        # cv2.imshow('object detection', cv2.resize(img, (800, 600)))
        return render_template('/index.html', data=[object_info, stroke_data])



@app.route("/", methods=['POST'])
def upload():
    if request.method == 'POST':
        pre_detection_img = Image.open(request.files['file'].stream)
        img, object_info, stroke_data = detector.detect_object(pre_detection_img)
        return render_template('/sketch.html', data=[object_info, stroke_data])

if __name__ == "__main__":
    app.run(debug=True)