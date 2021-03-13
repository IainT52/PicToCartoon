import cv2
import os
import numpy
from quickdraw import QuickDrawData

class Detector:
    def __init__(self):
        # Load a model imported from Tensorflow.
        frozen_ssd_model = os.path.join('models','ssd_mobilenet_model','frozen_inference_graph.pb')
        ssd_config = os.path.join('models','ssd_mobilenet_model','ssd_mobilenet_v1_coco_2017_11_17.pbtxt')
        self.tensorflowNet = cv2.dnn.readNetFromTensorflow(frozen_ssd_model, ssd_config)

        # Tensorflow accuracy threshold
        self.threshold = 0.5

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
    'suitcase': 'suitcase', 'frisbee': 'circle', 'skis': '', 'snowboard': '', 'sports ball': 'soccer ball', 'kite': 'scissors',
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
        img_height, img_width, channels = img.shape

        # Use the given image as input, which needs to be blob(s).
        self.tensorflowNet.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False))

        # Runs a forward pass to compute the net output.
        networkOutput = self.tensorflowNet.forward()

        # For mask rcnn model
        # networkOutput, mask = self.tensorflowNet.forward(["detection_out_final", "detection_masks"])

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
                obj_left = detection[3] * img_width
                obj_top = detection[4] * img_height
                obj_right = detection[5] * img_width
                obj_bottom = detection[6] * img_height
                # Object name, scale, and x,y offet
                name_of_object = self.classNames[detection[1]]
                xy_scale = self.get_object_scale(obj_left,obj_right,obj_top,obj_bottom,img_width,img_height)
                xy_normalized = self.normalize_object_coordinates(obj_left,obj_top,img_width,img_height)
                self.detected_objects.append({"name": name_of_object, "scale": xy_scale, "normalized": xy_normalized, "img_width":img_width, "img_height":img_height})

                # draw a red rectangle around detected objects
                cv2.rectangle(img, (int(obj_left), int(obj_top)), (int(obj_right), int(obj_bottom)), (0, 0, 255), thickness=2)
        
        # Resize the image
        # scaled_width = 1000
        # scaled_height = int(scaled_width * img_height / img_width)
        # img = cv2.resize(img, (scaled_width, scaled_height), interpolation = cv2.INTER_AREA)
        # cv2.imshow('image',img)
        # cv2.waitKey(0)
        
        strokes = self.draw_cartoon()
        object_info = self.detected_objects

        # Empty the detected objects for the next call
        self.detected_objects = []

        return img, object_info, strokes
    
    
    def get_object_scale(self, obj_left, obj_right, obj_top, obj_bottom, img_width, img_height):
        scale_x = (obj_right-obj_left)/img_width
        scale_y = (obj_bottom-obj_top)/img_height
        return [scale_x, scale_y]

    '''
    Example Input:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Lets say we want to normalize the cartoon point of (100,100) ->
        cartoon_img_width = 255
        cartoon_img_height = 255
        img_width = 2000
        img_height = 1300
        canvas_width = 1200
        canvas_height = 700
        img_scale_x = function call above ^ = 0.30
        img_scale_y = function call above ^ = 0.98
        obj_left = 1000
        obj_top = 20
        obj_bottom = 1300
        obj_right = 1600
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Determining the normalized coordinates for the cartoon drawing:
            - Call this function below to get the normalized x and y coordinates for the object: x_norm = 0.5 | y_norm = 0.015
            - x point scaled and normalized = ((cartoon_point_x / cartoon_img_width) * (img_scale_x * img_width)) + (x_norm*canvas_width) -> ((100/255)*.30*1200) + (.5*1200)
            - y point scaled and normalized = ((cartoon_point_y / cartoon_img_height) * (img_scale_y * img_height)) + (y_norm*canvas_height) -> ((100/255)*0.98*700) + (.015*700)

    '''
    def normalize_object_coordinates(self, obj_left, obj_top, img_width, img_height):
        x_normalized = obj_left/img_width
        y_normalized = obj_top/img_height
        return [x_normalized, y_normalized]

    def draw_cartoon(self):
        # Initialize a QuickDraw object to access the API
        qd = QuickDrawData()
        strokes_object_list = []
        # Get quickdraw cartoon drawings with object results
        for object in self.detected_objects:
            object = object["name"]
            qd_object = self.tensorflow_to_quickdraw_hash[object]
            if qd_object != "":
                cur_object = qd.get_drawing(qd_object)
                width, height = cur_object.image.size
                print(width, height)
                # Strokes
                strokes_object_list.append(cur_object.strokes)
            else:
                print(f"{object} is not a valid QuickDraw Image")
        return strokes_object_list