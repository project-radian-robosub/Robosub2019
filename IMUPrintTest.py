from simple_pid import PID
import time


def recenter(center, value):
    difference = value - center

    if abs(difference) > 180:
        return difference - (360 * (difference/abs(difference)))
    else:
        return difference


class IMU:

    def __init__(self, kp_x=0, ki_x=0, kd_x=0, kp_y=0, ki_y=0, kd_y=0, kp_z=0, ki_z=0, kd_z=0,
                 setpoint_x=0, setpoint_y=0, setpoint_z=0):

        self.pid_x = PID(kp_x, ki_x, kd_x, setpoint_x)
        self.pid_y = PID(kp_y, ki_y, kd_y, setpoint_y)
        self.pid_z = PID(kp_z, ki_z, kd_z, setpoint_z)

        self.kp_x = kp_x
        self.ki_x = ki_x
        self.kd_x = kd_x
        self.kp_y = kp_y
        self.ki_y = ki_y
        self.kd_y = kd_y
        self.kp_z = kp_z
        self.ki_z = ki_z
        self.kd_z = kd_z

        self.center_x = 0
        self.center_y = 0
        self.center_z = 0

    def get_angle_pid(self, given):
        pid_input_x = recenter(self.center_x, given)
        pid_input_y = recenter(self.center_y, given)
        pid_input_z = recenter(self.center_z, given)
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


imu = IMU(kp_z=1, kd_z=0)

val = 0
target = 180

timer1 = time.perf_counter()
timer2 = time.perf_counter()

while timer2 - timer1 < 1:
    print(imu.get_angle_pid(val)[2], recenter(imu.center_z, val), imu.center_z, val)
    time.sleep(0.1)
    timer2 = time.perf_counter()

imu.set_z(target)

while val < 360:
    print(imu.get_angle_pid(val)[2], recenter(imu.center_z, val), imu.center_z, val)
    time.sleep(0.01)
    val += 2

imu.set_z(0)

while val > 0:
    print(imu.get_angle_pid(val)[2], recenter(imu.center_z, val), imu.center_z, val)
    time.sleep(0.01)
    val -= 2
