import cv2
import numpy as np
import picamera
from time import sleep
from datetime import datetime
from pytz import timezone
#from PIL import Image
from datetime import date
import config
import glob
import os

print("before entering config.init_camera()")
camera = config.init_camera()
# write each function for each RAFCO command that is camera related 

 
# modify input, outputs 
# no input -> find the photo most recently taken, then perform modifications as needed 
'''
D4: change camera mode from color to grayscale
input: camera object from PiCamera, 
return camera object set to grayscale
'''
def greyscale2rgb():
    camera.color_effects = (128,128) # turn camera to black and white
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return camera

'''
F6: rotate camera 180 degrees
input: image, 
return its 180 degree rotation
'''
def rotate():
    list_of_files = glob.glob('./image_results/*.jpg') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    
    img = cv2.imread(latest_file) 
    rotated = cv2.rotate(img, cv2.ROTATE_180)
    file_path = latest_file.replace('.jpg','_rotated.jpg')
    cv2.imwrite(file_path, rotated)
    print(file_path)
    cv2.imwrite('./new.jpg', rotated)
    
    
    # using Pillow
    '''
    #read the image, not using OpenCV
    img = Image.open(latest_file)
    #rotate image
    angle = 45
    rotated = img.rotate(angle)
    file_path = latest_file.replace('.jpg','_rotated.jpg')
    rotated.save(file_path)
    '''
    return rotated 

# E5: change camera mode back from grayscale to color 
def to_color_mode():
    camera.color_effects = None
    return camera

# H8: remove all filters 
# remove filter on taking pictures
def remove_filter():
    camera.image_effect = None
    list_of_files = glob.glob('./image_results/*.jpg') # * means all if need specific format then *.csv
    list_of_files.sort(key=os.path.getctime)
    print(list_of_files)
    return camera


'''
G7: special effects filter to the image 
input: image
output: image with color space switched from RGB to BGR
other options for special effect: 
https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7
'''
def rgb2bgr(img):
    camera.image_effect = 'colorswap'
    list_of_files = glob.glob('./image_results/*.jpg') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    img = cv2.imread(latest_file)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    file_path = latest_file.replace('.jpg','_special.jpg')
    #file_path = str('./image_results/'+latest_file+'_special')
    cv2.imwrite(file_path, rgb)
    return rgb

# move picture taken to image_results
# C3: take picture
def take_picture():
    '''
    code moved to config.;y
    #create object for PiCamera class
    camera = picamera.PiCamera()
    #set resolution
    camera.resolution = (1024, 768)
    camera.brightness = 60
    '''
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
    #camera.close() 
    camera.annotate_text = annotation
    sleep(5)
    #store image
    camera.capture('./image_results'+annotation+'.jpeg')
    print("picture just captured")
    return camera


if __name__ == '__main__':
    # RGB to BGR Image Transformation Demo
    #img = cv2.imread("../../")
    #path = "./image_results/bgr_transform.jpg"
    #img_transformed = rgb2bgr(img)
    #cv2.imwrite(path, img_transformed)
    rotate()
    #cv2.imshow('RGB2BGR', img_transformed)
    #cv2.waitKey(0) 
    #cv2.destroyAllWindows() 
    print("executing tasks in imaging.py")
    

# https://www.nasa.gov/sites/default/files/atoms/files/2023_slhandbook_508.pdf

# add timestamp: format with date/time
# save to disk, rename with timestamp...
# C3 ~ H8
