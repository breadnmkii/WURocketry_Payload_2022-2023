# Default config file for initialization and configuration of Avionic 
# components

import board
import adafruit_bno055
import adafruit_bmp3xx

def init_avionics():
    i2c = board.I2C()
    bno055 = adafruit_bno055.BNO055_I2C(i2c)
    bmp388 = adafruit_bmp3xx.BMP3XX_I2C(i2c)

    print(bno055.accel_mode)
    print(bno055.accel_range)
    print(bno055.accel_bandwidth)

    print(bno055.gyro_mode)
    print(bno055.gyro_range)
    print(bno055.gyro_bandwidth)

    print(bno055.magnet_operation_mode)
    print(bno055.magnet_mode)
    print(bno055.magnet_rate)

    __config_BNO055(bno055)

    print(bno055.accel_mode)
    print(bno055.accel_range)
    print(bno055.accel_bandwidth)

    print(bno055.gyro_mode)
    print(bno055.gyro_range)
    print(bno055.gyro_bandwidth)

    print(bno055.magnet_operation_mode)
    print(bno055.magnet_mode)
    print(bno055.magnet_rate)


def __config_BNO055(sensor):
    # Change to configuration mode
    sensor.mode = adafruit_bno055.CONFIG_MODE
    ## Accelerometer Config
    sensor.accel_mode = adafruit_bno055.ACCEL_NORMAL_MODE
    sensor.accel_range = adafruit_bno055.ACCEL_16G
    sensor.accel_bandwidth = adafruit_bno055.ACCEL_500HZ
    ## Gyroscope Config
    sensor.gyro_mode = adafruit_bno055.GYRO_NORMAL_MODE
    sensor.gyro_range = adafruit_bno055.GYRO_2000_DPS
    sensor.gyro_bandwidth = adafruit_bno055.GYRO_523HZ
    ## Magnetometer Config
    sensor.magnet_operation_mode = adafruit_bno055.MAGNET_ACCURACY_MODE
    sensor.magnet_mode = adafruit_bno055.MAGNET_FORCEMODE_MODE
    sensor.magnet_rate = adafruit_bno055.MAGNET_30HZ

    # Revert back to operation mode    
    sensor.mode = adafruit_bno055.AMG_MODE
    print("Configured bno055!")

def __config_BMP388(sensor):

    print("Configured bmp388!")
    pass

if __name__ == '__main__':
    init_avionics()