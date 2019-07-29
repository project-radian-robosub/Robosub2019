
import time

import IMU
from PressureSensor import Pressure

p = Pressure()

while True:

    print(IMU.sensor.temperature)
    time.sleep(0.1)
