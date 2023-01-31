import cv2
import numpy as np
import picamera
from time import sleep
from datetime import datetime
from pytz import timezone
from datetime import date

#create object for PiCamera class
camera = picamera.PiCamera()
#set resolution
camera.resolution = (1024, 768)
camera.brightness = 60
# write each function for each RAFCO command that is camera related 

 
# modify input, outputs 
# no input -> find the photo most recently taken, then perform modifications as needed 
'''
D4: change camera mode from color to grayscale
input: image, 
return its grayscale version
'''
def greyscale2rgb(img):
    camera.color_effects = (128,128) # turn camera to black and white
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

'''
F6: rotate camera 180 degrees
input: image, 
return its 180 degree rotation
'''
def rotate(img):
    rotated = cv2.rotate(img, cv2.ROTATE_180)
    return rotated 

# E5: change camera mode back from grayscale to color 
# H8: remove all filters 
def get_original():
    return img

'''
G7: special effects filter to the image 
input: image
output: image with color space switched from RGB to BGR
'''
def rgb2bgr(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb

# C3: take picture
def take_picture():
    #create object for PiCamera class
    camera = picamera.PiCamera()
    #set resolution
    camera.resolution = (1024, 768)
    camera.brightness = 60


    # Get the timezone object for Chicago
    tz_cst = timezone('America/Chicago') 
    # Get the current time in CST
    datetime_cst = datetime.now(tz_cst)
    # Format the time as a string 
    local_time = datetime_cst.strftime("%H:%M:%S")
    # get date 
    today_date = date.today()
    #print("Today's date:", today_date, type(today_date))
    annotation = str(today_date)+'_'+local_time
    print("full annotation: ", annotation)
    #camera.start_preview()
    camera.annotate_text = annotation
    sleep(5)
    #store image
    camera.capture(annotation+'.jpeg')


if __name__ == '__main__':
    # RGB to BGR Image Transformation Demo
    #img = cv2.imread("../../")
    #path = "./image_results/bgr_transform.jpg"
    #img_transformed = rgb2bgr(img)
    #cv2.imwrite(path, img_transformed)
    take_picture()
    #cv2.imshow('RGB2BGR', img_transformed)
    #cv2.waitKey(0) 
    #cv2.destroyAllWindows() 
    

# https://www.nasa.gov/sites/default/files/atoms/files/2023_slhandbook_508.pdf

# add timestamp: format with date/time
# save to disk, rename with timestamp...
# C3 ~ H8
