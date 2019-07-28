import time

import IMU

while True:
    print(IMU.sensor.acceleration, IMU.print_corrected_acc())
    time.sleep(0.1)
