# Single-Image-Dehazing-Python
python implementation of the paper: "Efficient Image Dehazing with Boundary Constraint and Contextual Regularization"


## Quickstart
This library performs image dehazing.

## Installation

To install, run:
```
$ pip install image_dehazer
```

## Usage:
```Python
$ import image_dehazer										# Load the library

$ HazeImg = cv2.imread('image_path', 0)						# read input image
$ HazeCorrectedImg = image_dehazer.remove_haze(HazeImg)		# Remove Haze

$ cv2.imshow('input image', HazeImg);						# display the original hazy image
$ cv2.imshow('enhanced_image', HazeCorrectedImg);			# display the result
$ cv2.waitKey(0)											# hold the display window
```
As easy as that!