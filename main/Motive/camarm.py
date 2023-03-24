import time
from . import config
MARGIN = 2
current = 0
## Init servo components
# servo_config takes two params, GPIO for (r,w) respectively

# write/read parameters
servo, reader = config.servo_config(23,24)
lift_servo, lift_reader = config.servo_config(13,16)

def extend():
    lift_servo.set_speed(0.4)
    
    while(True):
        postion1 = get_angpos(lift_reader)

        time.sleep(.1)

        postion2 = get_angpos(lift_reader)

        if(abs(postion1-postion2) < 5):
            print("caught!")
            break

    lift_servo.stop()
    time.sleep(1)
    print("Stalled!")


# Calculate angular position (degrees)
def get_angpos_helper(read_dc):
    # Constants
   DC_MIN = 3.185 # / 10
   DC_MAX = 99.19 # / 10

   return ((read_dc - DC_MIN) * 360) / (DC_MAX - DC_MIN + 1)


#set a custom angle position
def set_angpos(moveto_angle):
    
    global current
    
    if moveto_angle < current:
        servo.set_speed(-0.2)   # @6v -0.15
    else:
        servo.set_speed(0.1)    # @6v 0.09


    curr_pos = get_angpos(reader)
    while (curr_pos > moveto_angle+MARGIN or curr_pos < moveto_angle-MARGIN):
        curr_pos = get_angpos(reader)
    
    current = moveto_angle
    servo.stop()


    
#return the current angular position
def get_angpos(given_reader):
    position = round((get_angpos_helper(given_reader.read()/10)), 2)


    return position


#set angular position to zero    
def set_zero():
    set_angpos(0)
    print("Set 360 Position to Zero Sucessfully")
    






    
def left_60():
    global current

    moveto_angle = current - 60

    if moveto_angle < 0:
        moveto_angle = moveto_angle + 360
    
    print("Moving Left! to ", moveto_angle)
    set_angpos(moveto_angle)






def right_60():
    global current

    moveto_angle = current + 60
    moveto_angle = moveto_angle % 360

    print("Moving Right! to ", moveto_angle)
    set_angpos(moveto_angle)


def main():
    left_60()
    right_60()

    print("stopped and waiting 2 seconds")
    time.sleep(2)
    servo.stop()
    print("extend!")
    extend()
    
if __name__ == '__main__':
    main()

