# Default config file for init/config of avionic components

import board
import adafruit_bno055
import adafruit_bmp3xx
import time
import math

def init_avionics():
    i2c = board.I2C()
    try:
        bno055 = adafruit_bno055.BNO055_I2C(i2c)
    except:
        print('enetered the except case')
        print("WARNING: BNO055 NOT INITIALIZED")
        bno055 = None
    
    try:
        bmp388 = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    except:
        print("WARNING: BMP388 NOT INITIALIZED")
        bmp388 = None

    
    __config_BNO055(bno055, adafruit_bno055.NDOF_MODE)
    __calibrate_BNO055(bno055)
    __config_BMP388(bmp388, 25)

    return(bno055, bmp388)

# NEED testing
def __calibrate_BNO055(bno055):
    SECOND_NS = 1_000_000_000
    NUM_READINGS = 1000000
    SAMPLE_FREQUENCY = 100   # in Hz
    DELTA_T = SECOND_NS/SAMPLE_FREQUENCY
    last_sample_T = time.monotonic_ns()

    start_sample_T = time.monotonic_ns()
    while (NUM_READINGS):

        this_sample_T = time.monotonic_ns()
        if (this_sample_T >= last_sample_T + DELTA_T):

            if (bno055.calibrated):
                # Read bno055 data
                print(f"time:{this_sample_T-start_sample_T}\tgyro:{bno055.gyro}\taccl:{bno055.linear_acceleration}\tmagn:{bno055.magnetic}")
                # the quaternion stuff will be deleted later
                if not None in bno055.quaternion:
                    quat = bno055.quaternion
                    [x, y, z, w] = quat
                    yy = y * y # 2 Uses below
                    roll = math.atan2(2 * (w* x + y * z), 1 - 2*(x * x + yy))
                    # clamping asin values
                    yaw = math.asin(max(-1, min(2 * w * y - x * z, 1)))
                    pitch = math.atan2(2 * (w* z + x * y), 1 - 2*(yy+z * z))

                    print('pitch, row, yaw:', pitch, roll, yaw)
                NUM_READINGS -= 1
            else:
                print(f'Calibration (s,g,a,m) {bno055.calibration_status}')
                start_sample_T = time.monotonic_ns()

            last_sample_T = this_sample_T

def __config_BNO055(sensor, mode):
    print("Configuring bno055...")

    if sensor == None:
        print('unable to create bno object')
        return
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
    sensor.mode = mode

    print("...set accel_mode:", sensor.accel_mode)
    print("...set accel_range:", sensor.accel_range)
    print("...set accel_bandwitdh:", sensor.accel_bandwidth)

    print("...set gyro_mode:", sensor.gyro_mode)
    print("...set gyro_range:", sensor.gyro_range)
    print("...set gyro_bandwitdth:", sensor.gyro_bandwidth)

    print("...set magnet_operation_mode:", sensor.magnet_operation_mode)
    print("...set magnet_mode:", sensor.magnet_mode)
    print("...set magnet_rate:", sensor.magnet_rate)

def __config_BMP388(sensor, avg_iter):
    print("Configuring BMP388...")

    avg = sum([sensor.pressure for _ in range(avg_iter)])/avg_iter
    sensor.sea_level_pressure = avg
    avg = sum([sensor.altitude for _ in range(avg_iter)])/avg_iter
    sensor.sea_level_altitude = avg # COULD BE BUGGY
    
    print("...set base MSL pressure to", avg)



if __name__ == '__main__':
    (bno, bmp) = init_avionics()
    
    print("RUNNING")
    print(bmp.altitude)