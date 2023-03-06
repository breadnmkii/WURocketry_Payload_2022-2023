# WURocketry_Payload_2022-2023
Electrical Team:
* Autumn
* Logan
* John

# Directories
## main
Directory for mission Payload code, no code tests in here!

## dev
Directory for all code tests of components, development, etc.

# SubDirectories
## Avionics
Software related to on-board avionics sensor collection components

## Imaging
Contains software related to configuring RPI camera and image filters




## Motive
Functionality for motor/servo and general electromotive tests

TODOS:
* verify that the angular position is actually accurate with how much the servo has moved.
* set the pigpio daemon to start on startup of rasberry pi 
* further discuss benefits of using 6V with a regulator for servo power to make sure it does not stall

Current Functionality and Notes:
* servo.py can find angles and stop the servo at them within a 2 degree margin of error
* slowest counterclockwise is -.2
* servo can run at 5V but preference is 6V
* slowest speed for rotation .1 clockwise 
* calibration library returns in scale of 1000 but we want 100 for percentage duty cycle scale 
* minimum duty cycle 3.185%
* maximum duty cycle 99.19%
	
Important Steps For Testing servo.py:
 1. start pigpio daemon before running script (sudo pigpiod)
 2. connect servo to 5V and ground
 3. feedback pin to broadcomm gpio 24
 4. control pin to broadcomm gpio 23 (right above feedback) 
 5. run servo.py (python3 servo.py)
	




## Radio
Provides functionality for running RTL-SDR based APRS reception of RF data

## Software-Control
Enables processing of RAFCO via a finite state machine for execution of Payload mission

# Dependencies
## System
- APRS Direwolf OS
- Adafruit Blinka configuration: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
	+ local install: python3 -m pip install Adafruit-Blinka RPi.GPIO
- I2C Clock Stretching: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/i2c-clock-stretching

## Avionics
- mathlib			(pip)
- adafruit-circuitpython-bno055	(pip)
- adafruit-circuitpython-bmp3xx	(pip)

## Imaging
- picamera			(pip)
- opencv-python-headless	(pip)
- numpy				(pip)
- pytz				(pip)


## Motive
(Servo)
- pigpio 			(apt): allows us to send pulse width modulation signals for servo control on the pi pins
- lib_para_servo_360 		(pip): controls for seeing position of servo and changing speeds

(Motor)
- adafruit-circuitpython-motorkit (pip)

## Radio
- adafruit-circuitpython-rfm9x	(pip)

## Software-Control
