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
from datetime import date


#create object for PiCamera class
camera = picamera.PiCamera()
#set resolution
camera.resolution = (1024, 768)
camera.brightness = 60


# Get the timezone object for Chicago
tz_cst = pytz.timezone('America/Chicago') 

# Get the current time in New York
datetime_cst = datetime.now(tz_cst)

local_time = datetime_cst.strftime("%H:%M:%S")
# Format the time as a string and print it
print("CST time:", local_time, type(local_time))

today = date.today()
print("Today's date:", today, type(today))



#camera.start_preview()
now = datetime.now()
trying = now.strftime("%H:%M:%S")
print(now)
#utc = timezone('UTC')
timezone = pytz.timezone("America/Chicago")
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
