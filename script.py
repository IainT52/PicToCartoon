classNames = {0: 'background',
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
object_hash = {}

file1 = open('objects.txt', 'r')
Lines = file1.readlines()
count = 0
# Strips the newline character
for line in Lines:
    object_hash[line.strip()] = count
    count += 1



ne_hash = {}
for i in classNames.keys():
    if classNames[i] in object_hash:
        ne_hash[classNames[i]] = classNames[i]
    else:
        ne_hash[classNames[i]] = ""
print(object_hash)

# Every key represents a tensorflow object and every value represents a matching quickdraw object
tensorflow_to_quickdraw_hash = {'background': '', 'person': '', 'bicycle': 'bicycle', 'car': 'car', 'motorcycle': '',
    'airplane': 'airplane', 'bus': 'bus', 'train': 'train', 'truck': 'truck', 'boat': '', 'traffic light': 'traffic light',
    'fire hydrant': 'fire hydrant', 'stop sign': 'stop sign', 'parking meter': '', 'bench': 'bench', 'bird': 'bird',
    'cat': 'cat', 'dog': 'dog', 'horse': 'horse', 'sheep': 'sheep', 'cow': 'cow', 'elephant': 'elephant', 'bear': 'bear',
    'zebra': 'zebra', 'giraffe': 'giraffe', 'backpack': 'backpack', 'umbrella': 'umbrella', 'handbag': '', 'tie': '',
    'suitcase': 'suitcase', 'frisbee': '', 'skis': '', 'snowboard': '', 'sports ball': '', 'kite': '',
    'baseball bat': 'baseball bat', 'baseball glove': '', 'skateboard': 'skateboard', 'surfboard': '', 'tennis racket': '',
    'bottle': '', 'wine glass': 'wine glass', 'cup': 'cup', 'fork': 'fork', 'knife': 'knife', 'spoon': 'spoon', 'bowl': '',
    'banana': 'banana', 'apple': 'apple', 'sandwich': 'sandwich', 'orange': '', 'broccoli': 'broccoli', 'carrot': 'carrot',
    'hot dog': 'hot dog', 'pizza': 'pizza', 'donut': 'donut', 'cake': 'cake', 'chair': 'chair', 'couch': 'couch',
    'potted plant': '', 'bed': 'bed', 'dining table': '', 'toilet': 'toilet', 'tv': '', 'laptop': 'laptop', 'mouse': 'mouse',
    'remote': '', 'keyboard': 'keyboard', 'cell phone': 'cell phone', 'microwave': 'microwave', 'oven': 'oven',
    'toaster': 'toaster', 'sink': 'sink', 'refrigerator': '', 'book': 'book', 'clock': 'clock', 'vase': 'vase',
    'scissors': 'scissors', 'teddy bear': '', 'hair drier': '', 'toothbrush': 'toothbrush'}