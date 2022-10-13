# WURocketry_Payload_2022-2023

## RF Module APRS CLI
rtl_fm -f 144.390M -s 22050 | multimon-ng -t raw -a AFSK1200 -f alpha /dev/stdin

# Directories
## Imaging
Contains software related to configuring RPI camera and image filters

## RF
Provides functionality for running RTL-SDR based APRS reception of RF data

## FSM
Enables processing of RAFCO via a finite state machine for execution of Payload mission