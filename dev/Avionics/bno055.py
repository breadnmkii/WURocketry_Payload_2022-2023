import time
import mathlib
import board
import math
import adafruit_bno055 as a_bno

## Units
#   - Acceleration:         m/s^2
#   - Magnetic Strength:    uT
#   - Angular Velocity:     rad/s

if __name__ == '__main__':
    i2c = board.I2C()
    bno055 = a_bno.BNO055_I2C(i2c)

    ### IMU Configuration
    # Change to configuration mode
    # bno055.mode = a_bno.CONFIG_MODE
    ## Accelerometer Config
    # bno055.accel_mode = a_bno.ACCEL_NORMAL_MODE
    # bno055.accel_range = a_bno.ACCEL_16G
    # bno055.accel_bandwidth = a_bno.ACCEL_500HZ
    ## Gyroscope Config
    # bno055.gyro_mode = a_bno.GYRO_NORMAL_MODE
    # bno055.gyro_range = a_bno.GYRO_2000_DPS
    # bno055.gyro_bandwidth = a_bno.GYRO_523HZ
    ## Magnetometer Config
    # bno055.magnet_operation_mode = a_bno.MAGNET_ACCURACY_MODE
    # bno055.magnet_mode = a_bno.MAGNET_FORCEMODE_MODE
    # bno055.magnet_rate = a_bno.MAGNET_30HZ

    # Revert back to operation mode    
    # bno055.mode = a_bno.AMG_MODE

    SECOND_NS = 1_000_000_000
    NUM_READINGS = 1000000
    SAMPLE_FREQUENCY = 100   # in Hz
    DELTA_T = SECOND_NS/SAMPLE_FREQUENCY
    last_sample_T = time.monotonic_ns()

    start_sample_T = time.monotonic_ns()
    while (NUM_READINGS):

        this_sample_T = time.monotonic_ns()
        if (this_sample_T >= last_sample_T + DELTA_T):

            # if (bno055.calibrated):
            if (bno055.calibration_status[3] == 3):
                # Read bno055 data
                # print(f"time:{this_sample_T-start_sample_T}\tgyro:{bno055.gyro}\taccl:{bno055.linear_acceleration}\tmagn:{bno055.magnetic}")
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
