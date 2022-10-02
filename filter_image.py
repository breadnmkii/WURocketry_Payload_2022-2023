import sys
import cv2
import numpy as np

'''

distortions possible: 
blurring image by filters
some geometric distortions 
https://www.image-engineering.de/library/image-quality/factors/1062-distortion

possible libraries:
image.convert() in pillow library 
color.rgb2gray() in skitit-image
cv2.imread() in OenCV library
Conversion Formula and Matplotlib library 


R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]
imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B

'''

img = cv2.imread("./stand_in.png")
cv2.imshow('Original', img)