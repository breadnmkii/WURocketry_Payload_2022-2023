#Working on RFM96w, reference it as RFM9x

import time
import datetime     # for testing
import busio
import board
from digitalio import DigitalInOut

# Import the RFM9x radio module.
import adafruit_rfm9x

"""
 Pins PHYSICAL HEADER NUMBERS
   19 - MOSI
   21 - MISO
   22 - RST
   23 - SCK
   26 - CS
   
"""

# Configure RFM9x LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Configure radio frequencies
rf_channel = 7
rf_freq = 434.550 + rf_channel * 0.1

def config_RFM96w():
    try:
        RFM96w = adafruit_rfm9x.RFM9x(spi, CS, RESET, rf_freq)
        RFM96w.tx_power = 23
        RFM96w.receive()
        print("RFM96w successfully set up")
        return RFM96w

    except RuntimeError as error:
        print("RFM96w set up is unsuccessful")