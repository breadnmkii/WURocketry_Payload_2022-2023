import time
import board
import adafruit_bmp3xx

## Units
#   - Temperature:  Celsius
#   - Pressure:     hPa
#   - Altitude:     m

if __name__ == '__main__':
    i2c = board.I2C()
    bmp388 = adafruit_bmp3xx.BMP3XX_I2C(i2c)

    ### BMP Configuration
    # Local Sea Level Pressure (mb)
    # Note: For final design, try initializing sea level pressure to initial pressure readings,
    #       to give relative altitude from base altitude of launch pad.
    # bmp388.sea_level_pressure = 1016
    bmp388.sea_level_pressure = bmp388.pressure

    NUM_READINGS = 25
    while(NUM_READINGS):
        
        # Read sensor data
        print(f"temp:{bmp388.temperature}\tpres:{bmp388.pressure}\talti:{bmp388.altitude}")

        NUM_READINGS -= 1