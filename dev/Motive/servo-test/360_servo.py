import lib_para_360_servo
import pigpio
import time
import math
import atexit

#Define GPIO pins that we will read and write to (Using GPIO numbers NOT pin numbers)
WHITE_CABLE_SIGNAL = 23
YELLOW_CABLE_FEEDBACK = 24

#Define the margin of error
MARGIN = 2

#global current angular position variable
current = 0


# Calculate angular position (degrees)
def get_angpos_helper(read_dc):
    # Constants
   DC_MIN = 3.185 # / 10
   DC_MAX = 99.19 # / 10

   return ((read_dc - DC_MIN) * 360) / (DC_MAX - DC_MIN + 1)


#set a custom angle position
def set_angpos(servo, moveto_angle):
    
    global current
    
    if moveto_angle < current:
        servo.set_speed(-0.2)   # @6v -0.15
    else:
        servo.set_speed(0.1)    # @6v 0.09


    curr_pos = get_angpos()
    while (curr_pos > moveto_angle+MARGIN or curr_pos < moveto_angle-MARGIN):
        curr_pos = get_angpos()
    
    current = moveto_angle
    servo.stop()


    
#return the current angular position
def get_angpos():
    position = round((get_angpos_helper(reader.read()/10)), 2)


    return position


#set angular position to zero    
def set_zero(servo):
    set_angpos(servo, 0)
    print("Set 360 Position to Zero Sucessfully")
    






    
def left_60(servo):
    global current

    moveto_angle = current - 60

    if moveto_angle < 0:
        moveto_angle = moveto_angle + 360
    
    print("Moving Left! to ", moveto_angle)
    set_angpos(servo, moveto_angle)






def right_60(servo):
    global current

    moveto_angle = current + 60
    moveto_angle = moveto_angle % 360

    print("Moving Right! to ", moveto_angle)
    set_angpos(servo, moveto_angle)





def exit_handler():
    
    servo.stop()
    pi.stop()
    print('Finished!')
  






if __name__ == '__main__':


    #init pigpio to access GPIO pins with PWM
    pi = pigpio.pi()

    #init servo and servo position reader from lib_para_360_servo
    servo = lib_para_360_servo.write_pwm(pi = pi, gpio = WHITE_CABLE_SIGNAL)
    reader = lib_para_360_servo.read_pwm(pi = pi, gpio = YELLOW_CABLE_FEEDBACK)

    #create a handler to run exit requirements
    atexit.register(exit_handler)


    #Buffer time for initializing library servo
    time.sleep(2)
    print("INIT")
    servo.stop()

    time.sleep(1)
    
    #if(get_angpos() > 5):
    set_zero(servo)

    time.sleep(1)
    print("60")
    left_60(servo)
    
    time.sleep(1)
    print("0")
    left_60(servo)
    
    time.sleep(1)
    left_60(servo)

    time.sleep(1)
    left_60(servo)

    time.sleep(1)
    left_60(servo)

    time.sleep(1)
    left_60(servo)

    time.sleep(1)
    left_60(servo)
    
    time.sleep(1)
    print("60")
    right_60(servo)
    
    time.sleep(1)
    print("0")
    right_60(servo)
    
    time.sleep(1)
    right_60(servo)

    time.sleep(1)
    right_60(servo)

    time.sleep(1)
    right_60(servo)

    time.sleep(1)
    right_60(servo)    