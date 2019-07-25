import time
import Control

while True:
    print(Control.imu.sensor.magnet)
    time.sleep(0.1)
