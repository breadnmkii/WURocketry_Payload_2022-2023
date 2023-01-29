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
#from pytz import timezone
import pytz

#create object for PiCamera class
camera = picamera.PiCamera()
#set resolution
camera.resolution = (1024, 768)
camera.brightness = 60
#central = timezone('US/Central')
#camera.start_preview()
now = datetime.now()
#utc = timezone('UTC')
timezone = pytz.timezone("America/Central")
now = timezone.localize(now)
print(now)
current_time = now.strftime("%H:%M:%S %Z")
#published_time = datetime.strptime(current_time, '%H:%M:%S %Z')
#published_gmt = published_time.replace(tzinfo=utc)
#published_cst = published_gmt.astimezone(central)
actual_time_published = current_time.strftime('%I:%M:%S %p %Z')
#add text on image
camera.annotate_text = actual_time_published
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
