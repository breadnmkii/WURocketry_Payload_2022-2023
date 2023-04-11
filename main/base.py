import datetime   
import time
from Radio import telemetry
from enums import *
f = open("Radio/rf_test.txt", "w+")
f.write(f"Collection started: {datetime.datetime.now()}\n")

# Telemetry
def telemetryRoutine():
    telemetry.recieveData()


def test_base():
    while (True):
        rx_data = telemetryRoutine()
        encoding = 0
        receive_time = time.time_ns()
        if rx_data != 0:
            encoding = str(Stage(rx_data[0]))+str(Movement(rx_data[1]))+str(Flight_Direction(rx_data[2]))+str(Verticality(rx_data[3]))+str(Separated(rx_data[4]))+str(Deployed(rx_data[5]))+str(Warn_Heat(rx_data[6]))+str(Warn_Camera(rx_data[7]))+str(Warn_Avionics(rx_data[8]))+str(Warn_Motive(rx_data[9]))
        f.write(f'{receive_time} <- {encoding}\n')
        print(f'{receive_time} <- {encoding}')  


if __name__ == '__main__':
    test_base()
