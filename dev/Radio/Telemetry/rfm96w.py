"""
 Pins
    GPIO 10 - MOSI
    GPIO 09 - MISO
    GPIO 11 - SCK
    GPIO 08 - CS
    GPIO 25 - RST

    print(board.MOSI)
    print(board.MISO)
    print(board.SCK)
    print(board.CE0)
    print(board.D25)
"""

import sys
import time
import busio
import board
from digitalio import DigitalInOut

# Import the RFM9x radio module
import adafruit_rfm9x

def transmit():
    # Initialize radio
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    RST = DigitalInOut(board.D25)
    CS = DigitalInOut(board.CE1)

    # Configure radio frequencies
    rf_channel = 7
    rf_freq = 434.550 + rf_channel * 0.1

    # Attempt setting up RFM9x Module
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RST, rf_freq)
        rfm9x.tx_power = 23
        print('RFM9x successfully set up!')

    except RuntimeError as error:
        print('Error in setting up RFM9x... check wiring.')
        return False
        

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
            tx_data = bytes(f'{time.time_ns()}\r\n', 'utf-8')
            rfm9x.send(tx_data)
            print(f'Sent -> {tx_data}')
            
            NUM_TRANSMITS -= 1
            last_sample_T = this_sample_T

def receiveLoop():
    pass

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
    main()