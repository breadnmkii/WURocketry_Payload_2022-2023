# RF Module APRS CLI
# Options (TODO: fill these out):
#   -f
#   -s
#   -t
#   -a
#   -f

rtl_fm -f 144.390M -s 22050 | multimon-ng -t raw -a AFSK1200 -f alpha /dev/stdin