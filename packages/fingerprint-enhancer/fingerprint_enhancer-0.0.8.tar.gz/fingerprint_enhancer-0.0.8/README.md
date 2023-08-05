# Fingerprint-Enhancement-Python

Uses oriented gabor filter bank to enhance the fingerprint image. The orientation of the gabor filters is decided by the orientation of ridges in the input image.


## Quickstart

This library performs fingerprint image enhancement which is necessary in biometric recognition systems applications.

## Installation
To install, run:
```
pip install fingerprint_enhancer
```

## Usage:
```Python
import fingerprint_enhancer								# Load the library
img = cv2.imread('image_path', 0)						# read input image
out = fingerprint_enhancer.enhance_Fingerprint(img)		# enhance the fingerprint image
cv2.imshow('enhanced_image', out);						# display the result
cv2.waitKey(0)											# hold the display window
```
As easy as that!
