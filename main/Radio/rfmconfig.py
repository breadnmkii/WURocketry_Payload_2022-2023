#Working on RFM96w, reference it as RFM9x

import time
import datetime     # for testing
import busio
import board
from digitalio import DigitalInOut

# Import the RFM9x radio module.
import adafruit_rfm9x

"""
 GPIO (not physical pin no)
   19 - MOSI
   21 - MISO
   ce0 - CS
   22 - EN  # not used?
   23 - RST
   11 - SCK
"""

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D23)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Configure radio frequencies
rf_channel = 5
rf_freq = 437.550 + rf_channel * 0.1
print(f'RFM_CONF: listening on: {rf_freq}')

def config_RFM96w():
    try:
        RFM96w = adafruit_rfm9x.RFM9x(spi, CS, RESET, rf_freq)
        RFM96w.tx_power = 23
        print("RFM96w successfully set up")
        return RFM96w

    except RuntimeError as error:
        print("RFM96w set up is unsuccessful")
        return False