import lib_para_360_servo
import pigpio
import time
import math



# Calculate angular position (degrees)
# ang = ((read_dc - dc_min) * 360) / (dc_max - dc_min + 1) 
def get_angpos_helper(read_dc):
    # Constants
   DC_MIN = 3.185 # / 10
   DC_MAX = 99.19 # / 10

   return ((read_dc - DC_MIN) * 360) / (DC_MAX - DC_MIN + 1)


#set a custom angle position
def set_angpos(servo, angle):
    servo.set_speed(0.1)
    curr_pos = math.floor(get_angpos_helper(reader.read()/10))
    while (curr_pos > angle+2 or curr_pos < angle-2):
        #print(curr_pos)
        curr_pos = math.floor(get_angpos(reader.read()/10))

    servo.stop()

    
#return the current angular position
def get_angpos():
    return math.floor(get_angpos_helper(reader.read()/10))


#set angular position to zero    
def set_zero(servo):
    set_angpos(servo, 0)
    print("Set 360 Position to Zero Sucessfully")

    
    
def left_60(servo):
    current = get_angpos()
    current = current - 60
    if current < 0:
        current = current + 360
    set_angpos(servo, current)
    

def right_60(servo):
    current = get_angpos()
    current = current + 60
    set_angpos(servo, current)
  

if __name__ == '__main__':
    #define GPIO for each servo to read from
    gpio_r_r = 24
    #define GPIO for each servo to write to
    gpio_r_w = 23
    pi = pigpio.pi()

    #### Create servo write_pwm class from library
    servo = lib_para_360_servo.write_pwm(pi = pi, gpio = gpio_r_w)
    reader = lib_para_360_servo.read_pwm(pi = pi, gpio = gpio_r_r)

    # Buffer time for initializing library servo
    time.sleep(1)
    servo.stop()



    servo.stop()
    pi.stop()


