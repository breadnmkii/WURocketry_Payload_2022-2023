# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,10) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)
print ("Waiting for 1 seconds")
time.sleep(1)
print("Running");

# Sweep duty values from 0 to 100 (1 sec)

for duty in range(40,60,1):
    print(f"Duty cycle of {duty:.2f}%")
    servo1.ChangeDutyCycle(duty/100)
    time.sleep(2)

'''
print("0.1")
servo1.ChangeDutyCycle(0.1)
time.sleep(1)
print("0.3")
servo1.ChangeDutyCycle(0.3)
time.sleep(1)
print("0.5")
servo1.ChangeDutyCycle(0.5)
time.sleep(1)
print("0.7")
servo1.ChangeDutyCycle(0.7)
time.sleep(1)
print("1")
servo.ChangeDutyCycle(1)
time.sleep(1)
'''

#Clean things up at the end
servo1.stop()
GPIO.cleanup()
print ("Goodbye")

