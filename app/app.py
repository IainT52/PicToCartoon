import cv2
import os
import sys
# Get the current file path and join it with the object detection file (allows us to be independent of the current working directory)
sys.path.append(os.path.join(os.path.dirname(__file__),'object_detection'))
print(os.path.join(os.path.dirname(__file__),'object_detection'))
from object_detection import Detector
from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__, template_folder='templates')
detector = Detector()
cap = cv2.VideoCapture(0)

@app.route("/")
def index():
    return render_template('/index.html', data=[0])


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
        return render_template('/index.html', data=[object_info, stroke_data])

if __name__ == "__main__":
    app.run(debug=True)