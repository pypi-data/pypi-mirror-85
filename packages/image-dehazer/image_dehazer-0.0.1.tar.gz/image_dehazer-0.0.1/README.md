# Single-Image-Dehazing-Python
python implementation of the paper: "Efficient Image Dehazing with Boundary Constraint and Contextual Regularization"


## Quickstart
This library performs image dehazing.

## Installation

To install, run:
```
pip install image_dehazer
```

## Usage:
```Python
import ImageDehazer										# Load the library

HazeImg = cv2.imread('image_path', 0)					# read input image
Dehazer = ImageDehazer()								# create the dehazer object
HazeCorrectedImg = Dehazer.remove_haze(HazeImg)			# call the dehazing function
cv2.imshow('enhanced_image', HazeCorrectedImg);			# display the result
cv2.waitKey(0)											# hold the display window
```
As easy as that!
