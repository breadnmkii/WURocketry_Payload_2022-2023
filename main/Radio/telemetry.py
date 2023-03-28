#Working on RFM96w, reference it as RFM9x

import time
import datetime     # for testing
import busio
import board
from . import rfmconfig
from digitalio import DigitalInOut

# Import the RFM9x radio module.
import adafruit_rfm9x

"""
 Pins
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

# Global RFM96w object to send/receieve data
RFM96W = rfmconfig.config_RFM96w()
f = open("rf_test.txt", "w+")
f.write(f"Collection started: {datetime.datetime.now()}\n")

def transmitData(str):
    # RX
    tx_packet =  bytes(f'{str}\r\n', 'utf-8')
    RFM96W.send(tx_packet)
    print(f'Sent -> {tx_packet}')

def recieveData():
    rx_packet = RFM96W.receive()
    if rx_packet:
        receive_time = time.time_ns()
        rx_data = str(rx_packet, "utf-8")
        f.write(f'{receive_time} <- {rx_data}\n')
        print(f'{receive_time} <- {rx_data}')  