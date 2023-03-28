#Working on RFM96w, reference it as RFM9x

import time
import datetime     # for testing
import busio
import board
from . import rfmconfig
from digitalio import DigitalInOut
from .. import enums
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
    print(tx_packet)
    RFM96W.send(tx_packet)
    print(f'Sent -> {tx_packet}')

def recieveData():
    rx_packet = RFM96W.receive()
    if rx_packet:
        receive_time = time.time_ns()
        rx_data = str(rx_packet, "utf-8")
        rx_data = int(rx_data.replace("|", "").replace(" ", ""))
        encoding = enums.Stage(rx_data[0])+enums.Movement(rx_data[1])+enums.Flight_Direction(rx_data[2])+enums.Verticality(rx_data[3])+enums.Separated(rx_data[4])+enums.Deployed(rx_data[5])+enums.Warn_Heat(rx_data[6])+enums.Warn_Camera(rx_data[7])+enums.Warn_Avionics(rx_data[8])+enums.Warn_Motive(rx_data[9])
        
        f.write(f'{receive_time} <- {encoding}\n')
        print(f'{receive_time} <- {encoding}')
        # below as integer, above try print as string
        #f.write(f'{receive_time} <- {rx_data}\n')
        #print(f'{receive_time} <- {rx_data}')  