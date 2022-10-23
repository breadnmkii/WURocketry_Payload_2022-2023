#!/bin/bash

while true
do 
rtl_fm -f 144.390M -s 22050 | multimon-ng -t raw -a AFSK1200 -f alpha /dev/stdin > data.txt
done
