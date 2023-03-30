import picamera
''' this seems to cause out of resources error
#create object for PiCamera class
camera = picamera.PiCamera()
#set resolution
camera.resolution = (1024, 768)
camera.brightness = 60
'''

def init_camera():
    #create object for PiCamera class
    camera = picamera.PiCamera()
    #set resolution
    camera.resolution = (1024, 768)
    camera.brightness = 60
    print("....camera mode: ", camera.sensor_mode)
    print("...setting camera resolution: ", camera.resolution)
    return camera