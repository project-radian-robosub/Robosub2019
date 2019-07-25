from IMU import IMU
from PressureSensor import Pressure
import MotorMovement

imu = IMU(kp_x=1, ki_x=0, kd_x=.2, kp_y=1, ki_y=0, kd_y=.2, kp_z=1, ki_z=0, kd_z=.2,
          kp_acc_x=0, ki_acc_x=0, kd_acc_x=0, kp_acc_y=0, ki_acc_y=0, kd_acc_y=0,
          setpoint_acc_x=0, setpoint_acc_y=0, setpoint_x=0, setpoint_y=0, setpoint_z=0)

pressure = Pressure(3, 0, 1, setpoint=990)

m2 = MotorMovement.motor_coroutine(0)
m3 = MotorMovement.motor_coroutine(1)
m4 = MotorMovement.motor_coroutine(2)
m5 = MotorMovement.motor_coroutine(3)
m6 = MotorMovement.motor_coroutine(4)
m7 = MotorMovement.motor_coroutine(5)

motor_powers = [0, 0, 0, 0, 0, 0]

acc_powers = [0, 0, 0, 0, 0, 0]
imu_powers = [0, 0, 0, 0, 0, 0]
pressure_powers = [0, 0, 0, 0, 0, 0]
move_powers = [0, 0, 0, 0, 0, 0]


def write_all(m2_val, m3_val, m4_val, m5_val, m6_val, m7_val):
    m2.send(m2_val)
    m3.send(m3_val)
    m4.send(m4_val)
    m5.send(m5_val)
    m6.send(m6_val)
    m7.send(m7_val)


def stop_all():
    m2.send(0)
    m3.send(0)
    m4.send(0)
    m5.send(0)
    m6.send(0)
    m7.send(0)


def set_acc_powers():
    x = int(imu.get_acc_pid()[0])
    y = int(imu.get_acc_pid()[1])
    acc_powers[0] = -y
    acc_powers[1] = -x
    acc_powers[4] = -x
    acc_powers[5] = -y


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

    m2.send(motor_powers[0])
    m3.send(motor_powers[1])
    m4.send(motor_powers[2])
    m5.send(motor_powers[3] * MotorMovement.reverse)
    m6.send(motor_powers[4])
    m7.send(motor_powers[5])


def acc_pid_x_enable(value, kp, ki, kd):
    if value:
        imu.set_acc_x_constants(kp, ki, kd)
    else:
        imu.set_acc_x_constants(0, 0, 0)


def acc_pid_y_enable(value, kp, ki, kd):
    if value:
        imu.set_acc_y_constants(kp, ki, kd)
    else:
        imu.set_acc_y_constants(0, 0, 0)