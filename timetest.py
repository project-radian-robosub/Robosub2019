import time

import IMU

while True:
    print(IMU.sensor.magnet)
    time.sleep(0.1)
