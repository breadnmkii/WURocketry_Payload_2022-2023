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
rf_channel = 7
rf_freq = 434.550 + rf_channel * 0.1

# Global RFM96w object to send/receieve data
RFM96W = rfmconfig.config_RFM96w()
f = open("rf_test.txt", "w+")
f.write(f"Collection started: {datetime.datetime.now()}\n")
if (RFM96W == False):
    f.write("RFM96W setup failed! No telemetry logged\n")

def transmitData(str):
    if (RFM96W != False and RFM96W != None):
        tx_packet =  bytes(f'{str}\r\n', 'utf-8')
        print(tx_packet)
        RFM96W.send(tx_packet)
        print(f'Sent -> {tx_packet}')
    else:
        print("Failed transmit!")
        return False

def recieveData():
    if (RFM96W != False and RFM96W != None):
        rx_packet = RFM96W.receive()
        if rx_packet:
            receive_time = time.time_ns()
            rx_data = str(rx_packet, "utf-8")
            f.write(f'{receive_time} <- {rx_data}\n')
            print(f'{receive_time} <- {rx_data}')  
    else:
        print("Failed receive!")
        return False