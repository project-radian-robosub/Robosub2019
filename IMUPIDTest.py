import IMU
import MotorMovement

imu = IMU.IMU(1, 0, 0, 0, 0, 0)

motor2 = MotorMovement.motor_coroutine(0)
motor7 = MotorMovement.motor_coroutine(5)
motor2_power = 0
motor7_power = 0


def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def stop_all():
    motor2.send(0)
    motor7.send(0)


try:
    motor2.send(0)
    motor7.send(0)
    while True:
        motor2_power = remap(imu.get_pid()[2], -180, 180, -100, 100)
        motor7_power = remap(imu.get_pid()[2], -180, 180, -100, 100) * -1
        motor2.send(int(motor2_power))
        motor7.send(int(motor7_power))

finally:
    stop_all()
    print("end")
