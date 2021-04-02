import os
import io
import sys
import cv2
import numpy
import base64
# Get the current file path and add it to the python sys path (allows us to use our object_detectin module independent of the current working directory)
sys.path.insert(0, os.path.dirname(__file__))
from object_detection import Detector

from flask import Flask, render_template, request, flash
from PIL import Image

app = Flask(__name__, template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

detector = Detector()


@app.route("/")
def index():
    return render_template('/index.html')


@app.route("/", methods=['POST'])
def upload():
    if request.method == 'POST':
        try:
            pre_detection_img = Image.open(request.files['file'].stream)
            img, object_info = detector.detect_object(pre_detection_img)
            string_img = convert_image_to_string(img)
            return render_template('/sketch.html', data=[object_info, string_img])

        except:
            print("Looks like you submitted an invalid file type!")
            flash('¯\_(ツ)_/¯   Looks like you submitted an invalid file type!')
            return render_template('/index.html')
            


@app.route("/default", methods=['POST'])
def submit_image():
    if request.method == 'POST':
        try:
            id = int(request.form['id'])
            img_path = os.path.join(os.path.dirname(__file__), "static", "images", f"default{str(id)}.jpg")
            pre_detection_img = Image.open(img_path)
            img, object_info = detector.detect_object(pre_detection_img)
            string_img = convert_image_to_string(img)
            return render_template('/sketch.html', data=[object_info, string_img])

        except:
            print("Invalid default image ID!")
            flash('¯\_(ツ)_/¯   Invalid default image ID!')
            return render_template('/index.html')


'''
This function takes a numpy array as input.
It converts the color of the array from BGR to RGB.
Then, the array is converted into a PIL image.
The PIL image is then converted to a base64 string.
'''
def convert_image_to_string(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(numpy.uint8(img)).convert('RGB')
    output = io.BytesIO()
    img.save(output, format="jpeg")
    return base64.b64encode(output.getvalue()).decode()
        

if __name__ == "__main__":
    app.run(debug=True)