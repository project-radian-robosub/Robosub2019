import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

while True:
    print(sensor.magnetometer, sensor.magnetic)
    time.sleep(.05)
