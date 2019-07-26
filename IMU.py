from simple_pid import PID
import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

def recenter(center, value):
    difference = value - center

    if abs(difference) > 180:
        return difference - (360 * (difference/abs(difference)))
    else:
        return difference


class IMU:

    def __init__(self, kp_x=0, ki_x=0, kd_x=0, kp_y=0, ki_y=0, kd_y=0, kp_z=0, ki_z=0, kd_z=0,
                 kp_acc_x=0, ki_acc_x=0, kd_acc_x=0, kp_acc_y=0, ki_acc_y=0, kd_acc_y=0,
                 setpoint_acc_x=0, setpoint_acc_y=0, setpoint_x=0, setpoint_y=0, setpoint_z=0):

        self.pid_x = PID(kp_x, ki_x, kd_x, setpoint_x, output_limits=(-60, 60))
        self.pid_y = PID(kp_y, ki_y, kd_y, setpoint_y, output_limits=(-60, 60))
        self.pid_z = PID(kp_z, ki_z, kd_z, setpoint_z, output_limits=(-60, 60))

        self.pid_acc_x = PID(kp_acc_x, ki_acc_x, kd_acc_x, setpoint_acc_x, output_limits=(-60, 60))
        self.pid_acc_y = PID(kp_acc_y, ki_acc_y, kd_acc_y, setpoint_acc_y, output_limits=(-60, 60))

        self.setpoint_x = setpoint_x
        self.setpoint_y = setpoint_y
        self.setpoint_z = setpoint_z

        self.setpoint_acc_x = setpoint_acc_x
        self.setpoint_acc_y = setpoint_acc_y

        self.kp_x = kp_x
        self.ki_x = ki_x
        self.kd_x = kd_x
        self.kp_y = kp_y
        self.ki_y = ki_y
        self.kd_y = kd_y
        self.kp_z = kp_z
        self.ki_z = ki_z
        self.kd_z = kd_z

        self.kp_acc_x = kp_acc_x
        self.ki_acc_x = ki_acc_x
        self.kd_acc_x = kd_acc_x
        self.kp_acc_y = kp_acc_y
        self.ki_acc_y = ki_acc_y
        self.kd_acc_y = kd_acc_y

    def get_angles(self):
        return sensor.euler

    def get_acc(self):
        return sensor.accelerometer

    def get_angle_pid(self):
        pid_input_x = recenter(self.setpoint_x, sensor.euler[2])
        pid_input_y = recenter(self.setpoint_y, sensor.euler[1])
        pid_input_z = recenter(self.setpoint_z, sensor.euler[0])
        pid_tuple = (self.pid_x(pid_input_x),
                     self.pid_y(pid_input_y),
                     self.pid_z(pid_input_z))
        return pid_tuple

    def get_acc_pid(self):
        pid_input_x = sensor.accelerometer[1]
        pid_input_y = sensor.accelerometer[0]
        pid_tuple = (self.pid_acc_x(pid_input_x),
                     self.pid_acc_y(pid_input_y))
        return pid_tuple

    def set_x(self, value):
        self.setpoint_x = value
        # self.pid_x.auto_mode = False
        # time.sleep(.1)
        self.pid_x.setpoint = self.setpoint_x
        # self.pid_x.auto_mode = True

    def set_y(self, value):
        self.setpoint_y = value
        self.pid_y.setpoint = self.setpoint_y

    def set_z(self, value):
        self.setpoint_z = value
        # self.pid_z.auto_mode = False
        # time.sleep(.1)
        self.pid_z.setpoint = self.setpoint_z
        # self.pid_z.auto_mode = False
        # self.pid_z.automode = True

    def set_acc_x(self, value):
        self.setpoint_acc_x = value
        self.pid_acc_x = PID(self.kp_acc_x, self.ki_acc_x, self.kd_acc_x, setpoint=self.setpoint_acc_x)

    def set_acc_y(self, value):
        self.setpoint_acc_x = value
        self.pid_acc_y = PID(self.kp_acc_y, self.ki_acc_y, self.kd_acc_y, setpoint=self.setpoint_acc_y)

    def set_acc_x_constants(self, kp, ki, kd):
        self.kp_acc_x = kp
        self.ki_acc_x = ki
        self.kd_acc_x = kd
        self.pid_acc_x = PID(self.kp_acc_x, self.ki_acc_x, self.kd_acc_x, setpoint=self.setpoint_acc_x)

    def set_acc_y_constants(self, kp, ki, kd):
        self.kp_acc_y = kp
        self.ki_acc_y = ki
        self.kd_acc_y = kd
        self.pid_acc_y = PID(self.kp_acc_y, self.ki_acc_y, self.kd_acc_y, setpoint=self.setpoint_acc_y)

