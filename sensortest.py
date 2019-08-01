
import time

import IMU
from PressureSensor import Pressure

p = Pressure()

while True:
    IMU.sensor.mode = IMU.sensor.NDOF_FMC_OFF_MODE
    print(p.get_val(), IMU.sensor.magnetic, IMU.sensor.euler)
    time.sleep(0.1)
