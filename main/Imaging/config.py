import picamera
#create object for PiCamera class
camera = picamera.PiCamera()
#set resolution
camera.resolution = (1024, 768)
camera.brightness = 60



def init_camera():
    #create object for PiCamera class
    camera = picamera.PiCamera()
    #set resolution
    camera.resolution = (1024, 768)
    camera.brightness = 60
    print("....camera mode: ", camera.sensor_mode)
    print("...setting camera resolution: ", camera.resolution)
    return camera

if __name__ == '__main__':
    camera = init_camera()
    print("CAMERA RUNNING")