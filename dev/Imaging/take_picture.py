'''
	capture images on Raspberry Pi using Pi Camera
	http://www.electronicwings.com
'''

# usr/lib/python3/dist-packages
# above: file path
import sys
sys.path.append('paste the copied path here')
import picamera
from time import sleep
from datetime import datetime

#create object for PiCamera class
camera = picamera.PiCamera()
#set resolution
camera.resolution = (1024, 768)
camera.brightness = 60
camera.start_preview()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
#add text on image
camera.annotate_text = current_time
sleep(5)
#store image

camera.capture(str(current_time)+'.jpeg')
camera.stop_preview()

def camera_time():
	#create object for PiCamera class
	camera = picamera.PiCamera()
	#set resolution
	camera.resolution = (1024, 768)
	camera.brightness = 60
	#add text on image
	camera.annotate_text = 'Hi Pi User'
	sleep(5)
	#store image
	camera.capture('image1.jpeg')
