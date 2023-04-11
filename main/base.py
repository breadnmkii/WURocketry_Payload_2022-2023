import datetime   
import time
from Radio import telemetry
from enums import *
f = open("Radio/rf_test.txt", "w+")
f.write(f"Collection started: {datetime.datetime.now()}\n")    


def test_base():
    while (True):
        rx_data = telemetry.recieveData()
        encoding = 0
        receive_time = time.time_ns()
        if rx_data != 0 and rx_data:
            encoding = '\n'+str(Stage(int(rx_data[0])))+'\n'+str(Movement(int(rx_data[1])))+'\n'+str(Flight_Direction(int(rx_data[2])))+'\n'+str(Verticality(int(rx_data[3])))+'\n'+str(Separated(int(rx_data[4])))+'\n'+str(Deployed(int(rx_data[5])))+'\n'+str(Warn_Heat(int(rx_data[6])))+'\n'+str(Warn_Camera(int(rx_data[7])))+'\n'+str(Warn_Avionics(int(rx_data[8])))+'\n'+str(Warn_Motive(int(rx_data[9])))
            f.write(f'{receive_time} <- {encoding}\n')
            print(f'\n{receive_time} <- {encoding}')  


if __name__ == '__main__':
    test_base()
