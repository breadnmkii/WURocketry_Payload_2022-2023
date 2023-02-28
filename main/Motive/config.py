import lib_para_360_servo
import pigpio
import time


def servo_config(x,y):

    #Define GPIO pins that we will read and write to (Using GPIO numbers NOT pin numbers)
    WHITE_CABLE_SIGNAL = x #23
    YELLOW_CABLE_FEEDBACK = y #24  

    #init pigpio to access GPIO pins with PWM
    pi = pigpio.pi()

    #init servo and servo position reader from lib_para_360_servo
    servo = lib_para_360_servo.write_pwm(pi = pi, gpio = WHITE_CABLE_SIGNAL)
    reader = lib_para_360_servo.read_pwm(pi = pi, gpio = YELLOW_CABLE_FEEDBACK)

    #create a handler to run exit requirements
    #atexit.register(exit_handler)


    #Buffer time for initializing library servo
    time.sleep(2)
    print("INIT")
    servo.stop()

    return servo,reader