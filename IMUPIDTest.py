import IMU
import MotorMovement

ser = MotorMovement.ser

imu = IMU.IMU(1, 0, 0, 0, 0, 0)

motor2 = MotorMovement.motor_coroutine(0)
motor3 = MotorMovement.motor_coroutine(1)
motor4 = MotorMovement.motor_coroutine(2)
motor5 = MotorMovement.motor_coroutine(3)
motor6 = MotorMovement.motor_coroutine(4)
motor7 = MotorMovement.motor_coroutine(5)
motor2_power = 0
motor3_power = 0
motor4_power = 0
motor5_power = 0
motor6_power = 0
motor7_power = 0


def wait_for_arduino():
    msg = ""
    while msg.find("ready") == -1:
        if ser.inWaiting() > 0:
            c = ser.read()
            msg += c.decode('utf-8')
            print("Arduino" + msg)


def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def stop_all():
    motor2.send(0)
    motor3.send(0)
    motor4.send(0)
    motor5.send(0)
    motor6.send(0)
    motor7.send(0)


try:
    wait_for_arduino()
    stop_all()
    while True:
        motor2_power = imu.get_pid()[2]
        motor7_power = -imu.get_pid()[2]
        motor2.send(int(motor2_power))
        motor7.send(int(motor7_power))
        motor3_power = -imu.get_pid()[1]
        motor6_power = imu.get_pid()[1]
        motor3.send(int(motor3_power))
        motor6.send(int(motor6_power))
        motor4_power = imu.get_pid()[0]
        motor5_power = -imu.get_pid()[0]
        motor4.send(int(motor4_power))
        motor5.send(int(motor5_power))

finally:
    stop_all()
    print("end")
