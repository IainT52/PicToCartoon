import cv2
import io
from object_detection import Detector
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__, template_folder='../templates')

@app.route("/")
def index():
    return render_template('/index.html')

@app.route("/", methods=['POST'])
def upload():
    if request.method == 'POST':
        detector = Detector()
        pre_detection_img = Image.open(request.files['file'].stream)
        img = detector.detect_object(pre_detection_img)
        return render_template('/index.html')


if __name__ == "__main__":
    app.run()