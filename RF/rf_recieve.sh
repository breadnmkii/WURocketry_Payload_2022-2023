#!/bin/bash

# RF Module APRS CLI
# Options (TODO: fill these out):
#   -f (frequency, given by nasa or universal APRS standard)
#   -s (sample rate, universal APRS standard)
#   -t (input type, in this case raw from transmission)
#   -a (specify demodulator, APRS standard AFSK1200)
#   -f (force data to be deocded using alpha mode)

# Note: This is not writing to file real time, prob need to open pipe in C program or something

while true
do 
rtl_fm -f 144.390M -s 22050 | multimon-ng -t raw -a AFSK1200 -f alpha /dev/stdin > data.txt
done
