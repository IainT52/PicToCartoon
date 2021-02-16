# PicToCartoon
Tensorflow 2 Neural Networks, OpenCV and Google QuickDraw come together to turn real life pictures into cartoon drawings. Using a pre-trained COCO model (SSD MobileNet V1) for object detection, this app can quickly identify 91 objects and translate them into their cartoon counterparts. 

- Requirements:
    * Python 3.8
    * Flask
    * OpenCV
    * QuickDraw
- Install dependencies using `pip install -r requirements.txt`.
- Run app from command line using `flask run`.
- Close the app using ctrl-C once the downloads have finished.


# How it works
#### Object Detection
- An image is submitted by the user and then passed through a TensorFlow 2 object detection model.
- Each detected object is surrounded by a 2D box to represent the area it takes up in the image.
- Each box is given a scale value corresponding to the size relative to the whole image. Ex. An object that takes up 25% of the entire image will have a scale = 0.25.
#### Fetching and Normalizing the QuickDraw Cartoon Drawings
- For each object, a matching cartoon drawing (the drawings stroke coordinates) is fetched from the QuickDraw API.
- The stroke coordinates for each cartoon drawing are scaled with each matching objects scale value.
- The stroke coordinates are offset by the location of ....To be continued 


# The Quick, Draw! Dataset
![photo](images/quickdraw.jpg)

The Quick Draw Dataset is a collection of 50 million drawings across [345 categories](categories.txt), contributed by players of the game [Quick, Draw!](https://quickdraw.withgoogle.com). The drawings were captured as timestamped vectors, tagged with metadata including what the player was asked to draw and in which country the player was located. You can browse the recognized drawings on [quickdraw.withgoogle.com/data](https://quickdraw.withgoogle.com/data).

We're sharing them here for developers, researchers, and artists to explore, study, and learn from. If you create something with this dataset, please let us know [by e-mail](mailto:quickdraw-support@google.com) or at [A.I. Experiments](https://aiexperiments.withgoogle.com/submit).

We have also released a tutorial and model for training your own drawing classifier on [tensorflow.org](https://www.tensorflow.org/tutorials/sequences/recurrent_quickdraw).

## The raw moderated dataset
The raw data is available as [`ndjson`](http://ndjson.org/) files seperated by category, in the following format: 

| Key          | Type                   | Description                                  |
| ------------ | -----------------------| -------------------------------------------- |
| key_id       | 64-bit unsigned integer| A unique identifier across all drawings.     |
| word         | string                 | Category the player was prompted to draw.    |
| recognized   | boolean                | Whether the word was recognized by the game. |
| timestamp    | datetime               | When the drawing was created.                |
| countrycode  | string                 | A two letter country code ([ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) of where the player was located. |
| drawing      | string                 | A JSON array representing the vector drawing |  


Each line contains one drawing. Here's an example of a single drawing:

```javascript
  { 
    "key_id":"5891796615823360",
    "word":"nose",
    "countrycode":"AE",
    "timestamp":"2017-03-01 20:41:36.70725 UTC",
    "recognized":true,
    "drawing":[[[129,128,129,129,130,130,131,132,132,133,133,133,133,...]]]
  }
```
