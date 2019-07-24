from serial import Serial
import MotorMovement
import IMU
import time

ser = Serial("/dev/ttyAM0", 9600)

m2 = MotorMovement.motor_coroutine(0)
m3 = MotorMovement.motor_coroutine(1)
m4 = MotorMovement.motor_coroutine(2)
m5 = MotorMovement.motor_coroutine(3)
m6 = MotorMovement.motor_coroutine(4)
m7 = MotorMovement.motor_coroutine(5)

kp = 0.5
ki = 0
kd = 0

imu = IMU.IMU(kp, ki, kd, 0, 0, 0)


def wait_for_arduino():
    msg = ""
    while msg.find("ready") == -1:
        if ser.inWaiting() > 0:
            c = ser.read()
            msg += c.decode('utf-8')
            print(msg)


def stop_all():
    m2.send(0)
    m3.send(0)
    m4.send(0)
    m5.send(0)
    m6.send(0)
    m7.send(0)


def write_all(m2_val, m3_val, m4_val, m5_val, m6_val, m7_val):
    m2.send(m2_val)
    m3.send(m3_val)
    m4.send(m4_val)
    m5.send(m5_val)
    m6.send(m6_val)
    m7.send(m7_val)
