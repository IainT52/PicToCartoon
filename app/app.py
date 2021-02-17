import json
from object_detection import Detector
from flask import Flask, render_template, request, send_file
from PIL import Image

app = Flask(__name__, template_folder='templates')
detector = Detector()

@app.route("/")
def index():
    return render_template('/index.html', data=[0])

@app.route("/", methods=['POST'])
def upload():
    if request.method == 'POST':
        pre_detection_img = Image.open(request.files['file'].stream)
        img, object_info, stroke_data = detector.detect_object(pre_detection_img)
        return render_template('/index.html', data=[object_info, stroke_data])


if __name__ == "__main__":
    app.run()