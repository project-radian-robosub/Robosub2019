import time

import IMU
import PressureSensor

while True:
    PressureSensor.p_sensor.read()
    print(PressureSensor.p_sensor.pressure(), IMU.sensor.acceleration, IMU.print_corrected_acc())
    time.sleep(0.1)
