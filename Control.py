from IMU import IMU
from PressureSensor import Pressure
import MotorMovement

imu = IMU(kp_x=0, ki_x=0, kd_x=0, kp_y=1, ki_y=0, kd_y=.2, kp_z=1, ki_z=.00, kd_z=.7)

pressure = Pressure(2.5, 0, 1.5, setpoint=920)

motors = MotorMovement.motor_generator()

motor_powers = [0, 0, 0, 0, 0, 0]

acc_powers = [0, 0, 0, 0, 0, 0]
imu_powers = [0, 0, 0, 0, 0, 0]
pressure_powers = [0, 0, 0, 0, 0, 0]
move_powers = [0, 0, 0, 0, 0, 0]


def write_all(m2_val, m3_val, m4_val, m5_val, m6_val, m7_val):
    MotorMovement.targets = [m2_val, m3_val, m4_val, m5_val, m6_val, m7_val]


def stop_all():
    MotorMovement.targets = [0, 0, 0, 0, 0, 0]


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
