import time

import IMU

while True:
    print(IMU.sensor.euler, IMU.sensor.acceleration)
    time.sleep(0.1)
