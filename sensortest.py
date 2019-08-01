
import time

import IMU
from PressureSensor import Pressure

p = Pressure()

while True:

    print(p.get_val(), IMU.sensor.magnetic, IMU.sensor.euler)
    time.sleep(0.1)
