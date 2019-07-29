
import time

import IMU
from PressureSensor import Pressure

p = Pressure()

while True:

    print(IMU.sensor.euler, IMU.sensor.magnetic)
    time.sleep(0.1)
