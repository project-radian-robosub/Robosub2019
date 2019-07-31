import time

import adafruit_bno055
import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

while True:
    print(sensor.calibration_status())
    time.sleep(.1)
