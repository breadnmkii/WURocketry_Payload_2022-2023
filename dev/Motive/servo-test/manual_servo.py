import lib_para_360_servo
import pigpio
import time
import math
import atexit
    


# Calculate angular position (degrees)
# ang = ((read_dc - dc_min) * 360) / (dc_max - dc_min + 1) 
def get_angpos_helper(read_dc):
    # Constants
   DC_MIN = 3.185 # / 10
   DC_MAX = 99.19 # / 10

   return ((read_dc - DC_MIN) * 360) / (DC_MAX - DC_MIN + 1)


#set a custom angle position
def set_angpos(servo, angle):
    curr_pos = get_angpos()
    angle = angle % 360

    if angle < curr_pos:
        servo.set_speed(-0.15)
    else:
        servo.set_speed(0.09)

    while (curr_pos > angle+margin or curr_pos < angle-margin):
        curr_pos = get_angpos()
    servo.stop()


    
#return the current angular position
def get_angpos():
    position = round((get_angpos_helper(reader.read()/10)), 2)

    print("Current Position ", position)

    return position


#set angular position to zero    
def set_zero(servo):
    set_angpos(servo, 0)
    print("Set 360 Position to Zero Sucessfully")
    
    
def left_60(servo):
    current = get_angpos()
    current = current - 60
    if current < 0:
        current = current + 360
    print("Moving Left!")
    set_angpos(servo, current)
    

def right_60(servo):
    current = get_angpos()
    current = current + 60
    print("Moving Right!")
    set_angpos(servo, current)

def exit_handler():
    
    servo.stop()
    pi.stop()
    print('Finished!')
  

if __name__ == '__main__':

    #Define GPIO pins that we will read and write to (Using GPIO numbers NOT pin numbers)
    WHITE_CABLE_SIGNAL = 23
    YELLOW_CABLE_FEEDBACK = 24

    #define margin of error
    margin = 2


    #init pigpio to access GPIO pins with PWM
    pi = pigpio.pi()

    #init servo and servo position reader from lib_para_360_servo
    servo = lib_para_360_servo.write_pwm(pi = pi, gpio = WHITE_CABLE_SIGNAL)
    reader = lib_para_360_servo.read_pwm(pi = pi, gpio = YELLOW_CABLE_FEEDBACK)

    print(servo)
    print(reader)
    print(reader.read())

    #create a handler to run exit requirements
    atexit.register(exit_handler)

    print("Pi Servo Controller | Enter speed range:")
    while (True):
         control = input(" : ")
         if (control == "exit"):
             servo.stop()
             break
         servo.set_speed(float(control))



    #Buffer time for initializing library servo
    #time.sleep(2)
    #print("INIT")

    #servo.set_speed(1)
    #time.sleep(4)
    #servo.stop()
    #set_zero(servo)
    #time.sleep(1)
    #right_60(servo)
    #time.sleep(1)
    #right_60(servo)
    #time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # right_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    # left_60(servo)
    # time.sleep(1)
    
    #while(1):
     #   val = int(input("Enter your value: "))
        
     #   set_angpos(servo, val)
     #   print(val)
      #  atexit.register(exit_handler)


    
    
    

