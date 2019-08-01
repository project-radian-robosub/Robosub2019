import math

import adafruit_bno055
import board
import busio
from simple_pid import PID

import Control

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)


def recenter(center, value):
    difference = value - center

    if abs(difference) > 180:
        return difference - (360 * (difference/abs(difference)))
    else:
        return difference


def gravity_correction(angle, value):
    gravity_component = 9.806 * math.sin(math.degrees(angle))
    correction = value - gravity_component
    return correction


def print_corrected_acc():
    pid_input_x = gravity_correction(sensor.euler[2], sensor.acceleration[1])
    pid_input_y = gravity_correction(sensor.euler[1], sensor.acceleration[0])
    return pid_input_x, pid_input_y


def check_calibration():
    if sensor.calibration_status:
        return True
    else:
        return False


class IMU:

    def __init__(self, kp_x=0, ki_x=0, kd_x=0, kp_y=0, ki_y=0, kd_y=0, kp_z=0, ki_z=0, kd_z=0, setpoint_x=0,
                 setpoint_y=0, setpoint_z=0, kp_acc_x=0, ki_acc_x=0, kd_acc_x=0, kp_acc_y=0, ki_acc_y=0,
                 kd_acc_y=0, setpoint_acc_x=0, setpoint_acc_y=0):

        self.pid_x = PID(kp_x, ki_x, kd_x, setpoint_x, output_limits=(-60, 60))
        self.pid_y = PID(kp_y, ki_y, kd_y, setpoint_y, output_limits=(-60, 60))
        self.pid_z = PID(kp_z, ki_z, kd_z, setpoint_z, output_limits=(-60, 60))

        self.kp_x = kp_x
        self.ki_x = ki_x
        self.kd_x = kd_x
        self.kp_y = kp_y
        self.ki_y = ki_y
        self.kd_y = kd_y
        self.kp_z = kp_z
        self.ki_z = ki_z
        self.kd_z = kd_z

        self.pid_acc_x = PID(kp_acc_x, ki_acc_x, kd_acc_x, setpoint_acc_x)
        self.pid_acc_y = PID(kp_acc_y, ki_acc_y, kd_acc_y, setpoint_acc_y)

        self.kp_acc_x = kp_acc_x
        self.ki_acc_x = ki_acc_x
        self.kd_acc_x = kd_acc_x
        self.kp_acc_y = kp_acc_y
        self.ki_acc_y = ki_acc_y
        self.kd_acc_y = kd_acc_y

        self.center_x = 0
        self.center_y = 0
        self.center_z = 0

    def get_angles(self):
        return sensor.euler

    def get_angle_pid(self):
        pid_input_x = recenter(self.center_x, sensor.euler[2])
        pid_input_y = recenter(self.center_y, sensor.euler[1])
        pid_input_z = recenter(self.center_z, sensor.euler[0])
        pid_tuple = (self.pid_x(pid_input_x),
                     self.pid_y(pid_input_y),
                     self.pid_z(pid_input_z))
        return pid_tuple

    def set_x(self, value):
        self.center_x = value

    def set_y(self, value):
        self.center_y = value

    def set_z(self, value):
        self.center_z = value
        Control.reset_n()

    def get_acc_pid(self):
        pid_input_x = sensor.acceleration[1]
        pid_input_y = sensor.acceleration[0]
        pid_tuple = (self.pid_acc_x(pid_input_x), self.pid_acc_y(pid_input_y))
        return pid_tuple

    def enable_acc_x_pid(self, enable):
        if enable:
            self.pid_acc_x = PID(self.kp_acc_x, self.ki_acc_x, self.kd_acc_x, 0)
        else:
            self.pid_acc_x = PID(0, 0, 0, 0)

    def enable_acc_y_pid(self, enable):
        if enable:
            self.pid_acc_y = PID(self.kp_acc_y, self.ki_acc_y, self.kd_acc_y, 0)
        else:
            self.pid_acc_y = PID(0, 0, 0, 0)
