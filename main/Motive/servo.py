import time
MARGIN = 2


def extend(servo):
    servo.set_speed(0.1)
    
    while(True):
        postion1 = get_angpos()

        time.sleep(.5)

        postion2 = get_angpos()

        if(abs(postion1-postion2) < 5):
            servo.stop()
            break

    print("Stalled!")


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
def get_angpos(reader):
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


