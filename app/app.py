import os
import sys
import json
# Get the current file path and add it to the python sys path (allows us to use our object_detectin module independent of the current working directory)
sys.path.insert(0, os.path.dirname(__file__))
from object_detection import Detector

from flask import Flask, render_template, request, flash
from PIL import Image

app = Flask(__name__, template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

detector = Detector()

cur_image_detected = None

@app.route("/")
def index():
    return render_template('/index.html')


@app.route("/", methods=['POST'])
def upload():
    global cur_image_detected
    if request.method == 'POST':
        try:
            pre_detection_img = Image.open(request.files['file'].stream)
            img, object_info, stroke_data = detector.detect_object(pre_detection_img)
            cur_image_detected = pre_detection_img
            return render_template('/sketch.html', data=[object_info, stroke_data])
        except:
            print("Looks like you submitted an invalid file type!")
            flash('¯\_(ツ)_/¯   Looks like you submitted an invalid file type!')
            return render_template('/index.html')


@app.route("/default", methods=['POST'])
def submit_image():
    global cur_image_detected
    if request.method == 'POST':
        try:
            id = int(request.form['id'])
            img_path = os.path.join(os.path.dirname(__file__), "static", "images", f"default{str(id)}.jpg")
            pre_detection_img = Image.open(img_path)
            img, object_info, stroke_data = detector.detect_object(pre_detection_img)
            cur_image_detected = pre_detection_img
            return render_template('/sketch.html', data=[object_info, stroke_data])
        except:
            print("Invalid default image ID!")
            flash('¯\_(ツ)_/¯   Invalid default image ID!')
            return render_template('/index.html')

@app.route("/getImage", methods=['GET'])
def get_image():
    global cur_image_detected
    if request.method == 'GET':
        # cur_image_detected.show()
        return json.dumps({'img':True})#cur_image_detected.tolist()
        

if __name__ == "__main__":
    app.run(debug=True)