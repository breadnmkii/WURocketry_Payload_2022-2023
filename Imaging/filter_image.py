import sys
import cv2
import numpy as np

# the current way of inputing image will be replaced by input from Raspberry Pi camera module
img = cv2.imread("./original.jpg")
path = "../image_results"
''' 
cv2.imshow('Original', img)

cv2.waitKey(0) 
cv2.destroyAllWindows() # image window destroyed after any key is pressed 
'''

'''
input: image, 
return its grayscale version
'''

def greyscale2rgb():
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

'''
input: image, 
return its 180 degree rotation
'''

def rotate():
    rotated = cv2.rotate(img, cv2.ROTATE_180)
    cv2.imwrite(path, rotated)
    return rotated 
'''
input: image, 
return its affine transformation (not obvious visually)
'''
def affine_transform():
    num_rows, num_cols = img.shape[:2]
    translation_matrix = np.float32([ [1,0,70], [0,1,110] ])
    img_translation = cv2.warpAffine(img, translation_matrix, (num_cols, num_rows), cv2.INTER_LINEAR)
    num_rows, num_cols = img.shape[:2]
    translation_matrix = np.float32([ [1,0,-30], [0,1,-50] ])
    img_translation = cv2.warpAffine(img_translation, translation_matrix, (num_cols + 70 + 30, num_rows + 110 + 50))
    cv2.imwrite(path, img_translation)
    return img_translation

'''
input: image, 
return its mirror image
'''
def mirror_transform():
    num_rows, num_cols = img.shape[:2]
    src_points = np.float32([[0,0], [num_cols-1,0], [0,num_rows-1]])
    dst_points = np.float32([[num_cols-1,0], [0,0], [num_cols-1,num_rows-1]])
    matrix = cv2.getAffineTransform(src_points, dst_points)
    img_afftran = cv2.warpAffine(img, matrix, (num_cols,num_rows))
    cv2.imwrite(path, img_afftran)
    return img_afftran

'''
input: image
output: image with color space switched from RGB to BGR
'''
def rgb2bgr():
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path, rgb)
    return rgb

'''
input: image
output: image transformed with projective method
'''
def projective_transform():
    num_rows, num_cols = img.shape[:2]
    src_points = np.float32([[0,0], [num_cols-1,0], [0,num_rows-1], [num_cols-1,num_rows-1]])
    dst_points = np.float32([[0,0], [num_cols-1,0], [int(0.33*num_cols),num_rows-1], [int(0.66*num_cols),num_rows-1]])
    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    img_protran = cv2.warpPerspective(img, projective_matrix, (num_cols,num_rows))
    cv2.imwrite(path, img_protran)
    return img_protran

def get_original():
    return img

'''
cv2.imshow('Grayscale', greyscale2rgb(img))
cv2.waitKey(0) 
cv2.destroyAllWindows() 

cv2.imshow('projected transform', projective_transform(img))
cv2.waitKey(0) 
cv2.destroyAllWindows() 
'''
