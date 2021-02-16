import cv2
import os
import numpy
from quickdraw import QuickDrawData

class Detector:
    def __init__(self):
        # Load a model imported from Tensorflow.
        frozenModel = '../ssd_mobilenet_model/frozen_inference_graph.pb'
        graph = '../ssd_mobilenet_model/ssd_mobilenet_v1_coco_2017_11_17.pbtxt'
        self.tensorflowNet = cv2.dnn.readNetFromTensorflow(frozenModel, graph)

        # Tensorflow accuracy threshold
        self.threshold = 0.4

        # List of dictionaries containg detected objects information.
        self.detected_objects = []

        # Label HashMap
        self.classNames = {0: 'background',
                    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
                    7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
                    13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
                    18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
                    24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
                    32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
                    37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
                    41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
                    46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
                    51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
                    56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
                    61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
                    67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
                    75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
                    80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
                    86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}
        # Tensorflow to QuickDraw HashMap
        self.tensorflow_to_quickdraw_hash = {'background': '', 'person': 'face', 'bicycle': 'bicycle', 'car': 'car', 'motorcycle': 'motorbike',
    'airplane': 'airplane', 'bus': 'bus', 'train': 'train', 'truck': 'truck', 'boat': 'sailboat', 'traffic light': 'traffic light',
    'fire hydrant': 'fire hydrant', 'stop sign': 'stop sign', 'parking meter': '', 'bench': 'bench', 'bird': 'bird',
    'cat': 'cat', 'dog': 'dog', 'horse': 'horse', 'sheep': 'sheep', 'cow': 'cow', 'elephant': 'elephant', 'bear': 'bear',
    'zebra': 'zebra', 'giraffe': 'giraffe', 'backpack': 'backpack', 'umbrella': 'umbrella', 'handbag': 'purse', 'tie': 'bowtie',
    'suitcase': 'suitcase', 'frisbee': 'circle', 'skis': '', 'snowboard': '', 'sports ball': 'soccer ball', 'kite': '',
    'baseball bat': 'baseball bat', 'baseball glove': '', 'skateboard': 'skateboard', 'surfboard': '', 'tennis racket': 'tennis racquet',
    'bottle': 'wine bottle', 'wine glass': 'wine glass', 'cup': 'cup', 'fork': 'fork', 'knife': 'knife', 'spoon': 'spoon', 'bowl': '',
    'banana': 'banana', 'apple': 'apple', 'sandwich': 'sandwich', 'orange': '', 'broccoli': 'broccoli', 'carrot': 'carrot',
    'hot dog': 'hot dog', 'pizza': 'pizza', 'donut': 'donut', 'cake': 'cake', 'chair': 'chair', 'couch': 'couch',
    'potted plant': 'house plant', 'bed': 'bed', 'dining table': 'table', 'toilet': 'toilet', 'tv': 'television', 'laptop': 'laptop', 'mouse': 'mouse',
    'remote': 'remote control', 'keyboard': 'keyboard', 'cell phone': 'cell phone', 'microwave': 'microwave', 'oven': 'oven',
    'toaster': 'toaster', 'sink': 'sink', 'refrigerator': '', 'book': 'book', 'clock': 'clock', 'vase': 'vase',
    'scissors': 'scissors', 'teddy bear': 'teddy-bear', 'hair drier': '', 'toothbrush': 'toothbrush'}


    def detect_object(self, img):
        # Input image
        img = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape

        # Use the given image as input, which needs to be blob(s).
        self.tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

        # Runs a forward pass to compute the net output.
        networkOutput = self.tensorflowNet.forward()

        ''' 
        Loop over the detected objects
            Detection Indexes:
            0: (not used)
            1: the identifier of the object's class ex. 5 = 'airplane'
            2: the accuracy (score) of the object detected
            3: dist of object from the left
            4: dist of object from the top
            5: dist of object from the right
            6: dist of object from the bottom
        '''
        for detection in networkOutput[0, 0]:

            score = float(detection[2])
            if score > self.threshold:

                # Object dimensions
                left = detection[3] * width
                top = detection[4] * height
                right = detection[5] * width
                bottom = detection[6] * height

                # Object name and scale
                name_of_object = self.classNames[detection[1]]
                scale = self.get_image_scale(left,right,top,bottom,width,height)
                self.detected_objects.append({"name": name_of_object, "scale": scale})

                # draw a red rectangle around detected objects
                cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), thickness=2)
        
        # Resize the image
        img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)
        
        self.draw_cartoon()
        # Show the image with a rectagle surrounding the detected objects
        cv2.imshow('Image', img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return img
    
    def get_image_scale(self, left, right, top, bottom, width, height):
        img_area = width*height
        object_area = (bottom-top)*(right-left)
        return object_area/img_area
    

    def draw_cartoon(self):
        # Initialize a QuickDraw object to access the API
        qd = QuickDrawData()

        # Get quickdraw cartoon drawings with object results
        for object in self.detected_objects:
            object = object["name"]
            qd_object = self.tensorflow_to_quickdraw_hash[object]
            if qd_object != "":
                cur_object = qd.get_drawing(qd_object, 1)
                cur_object.image.show()
                # Strokes
                for stroke in cur_object.strokes:
                    for x, y in stroke:
                        pass
                        # print("x={} y={}".format(x, y))
            else:
                print(f"{object} is not a valid QuickDraw Image")
        return