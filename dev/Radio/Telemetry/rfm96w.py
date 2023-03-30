"""
  Motor Hat No (not physical pin no)
   19 - MOSI
   21 - MISO
   ce0 - CS
   22 - EN  # not used?
   23 - RST
   11 - SCK
"""

import sys
import time
import datetime
import busio
import board
from digitalio import DigitalInOut

# Import the RFM9x radio module
import adafruit_rfm9x

def transmit():        

    print("Transmitting...")
    SECOND_NS = 1_000_000_000
    NUM_TRANSMITS = 25
    TRANSMIT_FREQUENCY = 1   # in Hz
    DELTA_T = SECOND_NS/TRANSMIT_FREQUENCY
    last_sample_T = time.monotonic_ns()

    while (NUM_TRANSMITS):
        this_sample_T = time.monotonic_ns()

        # Transmit
        if (this_sample_T >= last_sample_T + DELTA_T):
            data = time.time_ns()

            tx_data = bytes(f'{data}\r\n', 'utf-8')
            rfm9x.send(tx_data)
            print(f'Sent -> {tx_data}')
            
            NUM_TRANSMITS -= 1
            last_sample_T = this_sample_T

def receiveLoop():
    print("Receiving...")
    f = open("rf_receive.log", "w+")
    f.write(f"Collection log started: {datetime.datetime.now()}\n")
    
    while True:
        # Receive
        rx_packet = rfm9x.receive()
        if rx_packet:
            receive_time = time.time_ns()
            rx_data = str(rx_packet, "utf-8")

            f.write(f'{receive_time} <- {rx_data}\n')
            print(f'{receive_time} <- {rx_data}')

def main():
    if (len(sys.argv) != 2):
        print("usage:", sys.argv[0],"<transmit><receive>")
        return False
    
    if (sys.argv[1].lower() == "transmit"):
        transmit()
    elif (sys.argv[1].lower() == "receive"):
        receiveLoop()
    else:
        print("Unrecognized argument")
        return False

if __name__ == '__main__':
    # Initialize radio
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    RST = DigitalInOut(board.D23)
    CS = DigitalInOut(board.CE0)

    # Configure radio frequencies
    rf_channel = 7
    rf_freq = 434.550 + rf_channel * 0.1

    # Attempt setting up RFM9x Module
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RST, rf_freq)
        rfm9x.tx_power = 23
        print('RFM9x successfully set up!')
        main()

    except RuntimeError as error:
        print('Error in setting up RFM9x... check wiring.')