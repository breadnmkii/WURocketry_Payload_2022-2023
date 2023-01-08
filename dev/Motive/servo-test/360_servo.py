import lib_para_360_servo
import pigpio
import time
import math


# Calculate angular position (degrees)
# ang = ((read_dc - dc_min) * 360) / (dc_max - dc_min + 1) 
def get_angpos(read_dc):
    # Constants
   DC_MIN = 3.185 # / 10
   DC_MAX = 99.19 # / 10

   return ((read_dc - DC_MIN) * 360) / (DC_MAX - DC_MIN + 1)

def set_angpos(servo, angle):
    servo.set_speed(0.1)
    curr_pos = math.floor(get_angpos(reader.read()/10))
    while (curr_pos > angle+2 or curr_pos < angle-2):
        #print(curr_pos)
        curr_pos = math.floor(get_angpos(reader.read()/10))

    servo.stop()


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


    # Test 60 degree intervals
    for i in range(0, 360, 60):
        print("Setting angle to", i)
        set_angpos(servo, i)
        time.sleep(3)




    # Set servo speed for calibration
    # servo.set_speed(0.2)

    # Calibrate servos
    # wheel = lib_para_360_servo.calibrate_pwm(pi = pi, gpio = gpio_r_r)

    # print(get_angpos(reader.read()/10))
    # servo.set_speed(0.1)
    # time.sleep(0.5)
    # print(get_angpos(reader.read()/10))

    # time.sleep(0.5)
    # print(get_angpos(reader.read()/10))

    # time.sleep(0.5)
    # print(get_angpos(reader.read()/10))

    # time.sleep(0.5)
    # print(get_angpos(reader.read()/10))

    # Cleanup
    servo.stop()
    pi.stop()

"""

print("Calibrating")
wheel = lib_para_360_servo.calibrate_pwm(pi = pi, gpio = gpio_r_r)
servo.set_speed(0)
#http://abyz.me.uk/rpi/pigpio/python.html#stop
pi.stop()
"""
