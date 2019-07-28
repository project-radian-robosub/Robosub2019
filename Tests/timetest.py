import time

import IMU

while True:
    print(IMU.sensor.magnetic)
    time.sleep(0.1)
