import math

import IMU
import MotorMovement
from PressureSensor import Pressure

imu = IMU.IMU(kp_x=0, ki_x=0, kd_x=0, kp_y=1, ki_y=0, kd_y=.2, kp_z=1, ki_z=.00, kd_z=.7,
              kp_acc_x=0, ki_acc_x=0, kd_acc_x=0, kp_acc_y=0, ki_acc_y=0, kd_acc_y=0)

print(IMU.sensor.euler, IMU.sensor.acceleration)

pressure = Pressure(2.5, 0, 1.5, setpoint=1000)

motors = MotorMovement.motor_generator()

motor_powers = [0, 0, 0, 0, 0, 0]

acc_powers = [0, 0, 0, 0, 0, 0]
imu_powers = [0, 0, 0, 0, 0, 0]
pressure_powers = [0, 0, 0, 0, 0, 0]
move_powers = [0, 0, 0, 0, 0, 0]

n = 0


def write_all(m2_val, m3_val, m4_val, m5_val, m6_val, m7_val):
    MotorMovement.targets = [m2_val, m3_val, m4_val, m5_val, m6_val, m7_val]


def stop_all():
    MotorMovement.targets = [0, 0, 0, 0, 0, 0]
    max_val = 0
    index = 0
    for i in range(len(MotorMovement.current_vals)):
        if abs(MotorMovement.current_vals[i]) > max_val:
            max_val = abs(MotorMovement.current_vals[i])
            index = i
    while abs(MotorMovement.current_vals[index]) > 0:
        motors.__next__()


def set_acc_powers():
    x = int(imu.get_acc_pid()[0])
    y = int(imu.get_acc_pid()[1])
    acc_powers[0] = y
    acc_powers[1] = -x
    acc_powers[4] = -x
    acc_powers[5] = y


def set_imu_powers():
    x = int(imu.get_angle_pid()[0])
    y = int(imu.get_angle_pid()[1])
    z = int(imu.get_angle_pid()[2])
    imu_powers[0] = z
    imu_powers[1] = x
    imu_powers[2] = y
    imu_powers[3] = -y
    imu_powers[4] = -x
    imu_powers[5] = -z


def set_pressure_powers():
    pid = int(pressure.get_pid())
    pressure_powers[2] = -pid
    pressure_powers[3] = -pid


def set_move_powers(m2_val, m3_val, m4_val, m5_val, m6_val, m7_val):
    move_powers[0] = m2_val
    move_powers[1] = m3_val
    move_powers[2] = m4_val
    move_powers[3] = m5_val
    move_powers[4] = m6_val
    move_powers[5] = m7_val


def set_motor_powers():
    for i in range(len(motor_powers)):
        motor_powers[i] = 0
    for i in range(len(motor_powers)):
        motor_powers[i] += acc_powers[i]
        motor_powers[i] += imu_powers[i]
        motor_powers[i] += pressure_powers[i]
        motor_powers[i] += move_powers[i]

    max_pow = 0

    for i in range(len(motor_powers)):
        if abs(motor_powers[i]) > max_pow:
            max_pow = abs(motor_powers[i])

    if abs(max_pow) > 100:
        for i in range(len(motor_powers)):
            motor_powers[i] = MotorMovement.remap(motor_powers[i], -abs(max_pow), abs(max_pow), -100, 100)

    motor_powers[3] = motor_powers[3] * MotorMovement.reverse

    MotorMovement.targets = motor_powers

    motors.__next__()

    if not IMU.check_calibration():
        MotorMovement.GPIO.output(40, MotorMovement.GPIO.LOW)


def calculate_mag_error():
    global n
    n += math.atan(IMU.sensor.magnetic[1] / IMU.sensor.magnetic[0])
    mag_avg = n / 2
    error = (imu.center_z - 90) - mag_avg
    new_tar = imu.center_z + error
    return error
    '''
    if new_tar < 0:
        new_tar += 360
    elif new_tar >= 360:
        new_tar -= 360
    return new_tar
    '''


def get_n():
    return n


def reset_n():
    global n
    n = 0
