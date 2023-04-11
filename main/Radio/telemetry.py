#Working on RFM96w, reference it as RFM9x

import time
#import datetime     # for testing
import busio
import board
from . import rfmconfig
from digitalio import DigitalInOut
import sys
#from main import enums  # this would throw import errors
# Import the RFM9x radio module.
import adafruit_rfm9x
#sys.path.append('/home/pi/WURocketry_Payload_2022-2023')
#from main.enums import Stage, Movement, Flight_Direction, Verticality, Separated, Deployed, Warn_Heat, Warn_Camera, Warn_Avionics, Warn_Motive
#from main.enums import System_Flags

# Global RFM96w object to send/receieve data
RFM96W = rfmconfig.config_RFM96w()
#f = open("rf_test.txt", "w+")
#f.write(f"Collection started: {datetime.datetime.now()}\n")
if (RFM96W == False):
    f.write("RFM96W setup failed! No telemetry logged\n")

def transmitData(str):
    if (RFM96W != False and RFM96W != None):
        tx_packet =  bytes(f'{str}\r\n', 'utf-8')
        RFM96W.send(tx_packet)
        print(f'Sent -> {tx_packet}')
    else:
        print("Failed transmit!")
        return False

def recieveData():
    rx_packet = RFM96W.receive()
    if rx_packet:
        receive_time = time.time_ns()
        rx_data = str(rx_packet, "utf-8")

        rx_bitmask = rx_data.split(" ")[2]
        # print(rx_bitmask)
        # print(f'in telemetry.py {receive_time} <- {rx_data}')
        return rx_bitmask


        #encoding = str(Stage(rx_data[0]))+str(Movement(rx_data[1]))+str(Flight_Direction(rx_data[2]))+str(Verticality(rx_data[3]))+str(Separated(rx_data[4]))+str(Deployed(rx_data[5]))+str(Warn_Heat(rx_data[6]))+str(Warn_Camera(rx_data[7]))+str(Warn_Avionics(rx_data[8]))+str(Warn_Motive(rx_data[9]))
        #f.write(f'{receive_time} <- {encoding}\n')
        #print(f'{receive_time} <- {encoding}')
        # below as integer, above try print as string
        #f.write(f'{receive_time} <- {rx_data}\n')
        #print(f'{receive_time} <- {rx_data}')
    return 0


'''
def decode_enums(raw):
    strings = ""
    raw[]
    return strings
'''

