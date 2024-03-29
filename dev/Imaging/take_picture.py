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
from pytz import timezone
from datetime import date


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
#print("CST time:", local_time, type(local_time))
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
# camera.stop_preview()

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
