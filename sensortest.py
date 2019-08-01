
import time
import adafruit_bno055
import IMU
import MotorMovement
from PressureSensor import Pressure

p = Pressure()

while True:
    if MotorMovement.imu.sensor.calibration_status[3] > 2:
        MotorMovement.GPIO.output(40, MotorMovement.GPIO.HIGH)
    # IMU.sensor.mode = adafruit_bno055.ACCGYRO_MODE
    # print(IMU.sensor.mode)
    print(p.get_val(), IMU.sensor.euler)
    time.sleep(0.1)
