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
- mathlib
- adafruit-circuitpython-bno055
- adafruit-circuitpython-bmp3xx

## Imaging
- picamera
- cv2
- numpy

## Motive

## Radio

## Software-Control
