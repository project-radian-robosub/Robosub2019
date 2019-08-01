
import time

import IMU
import MotorMovement
from PressureSensor import Pressure

p = Pressure()

while True:
    if MotorMovement.imu.sensor.calibration_status[3] > 2:
        MotorMovement.GPIO.output(40, MotorMovement.GPIO.HIGH)
    IMU.sensor.mode = IMU.sensor.NDOF_FMC_OFF_MODE
    print(p.get_val(), IMU.sensor.magnetic, IMU.sensor.euler)
    time.sleep(0.1)
