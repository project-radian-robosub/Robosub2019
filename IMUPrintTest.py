from simple_pid import PID


def recenter(center, value):
    difference = value - center
    threshold = 0

    if center < 180:
        threshold = center + 180
    elif center >= 180:
        threshold = center - 180

    if center > value > threshold:
        return difference
    elif value > center > threshold:
        return difference
    elif value > threshold > center:
        return difference - 360
    elif threshold > value > center:
        return difference
    elif threshold > center > value:
        return difference
    elif center > threshold > value:
        return difference + 360
    elif value == threshold:
        return difference
    else:
        return 0


class IMU:
    invalue = 0
    kp = 0
    ki = 0
    kd = 0
    setpoint_x = 0
    setpoint_y = 0
    setpoint_z = 0

    def __init__(self, kp, ki, kd, setpoint_x=0, setpoint_y=0, setpoint_z=0):
        self.pid_x = PID(kp, ki, kd, setpoint_x)
        self.pid_y = PID(kp, ki, kd, setpoint_y)
        self.pid_z = PID(kp, ki, kd, setpoint_z)
        self.setpoint_x = setpoint_x
        self.setpoint_y = setpoint_y
        self.setpoint_z = setpoint_z
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def get_pid(self):
        pid_input_x = recenter(self.setpoint_x, self.invalue)
        pid_input_y = recenter(self.setpoint_y, self.invalue)
        pid_input_z = recenter(self.setpoint_z, self.invalue)
        pid_tuple = (self.pid_x(pid_input_x),
                     self.pid_y(pid_input_y),
                     self.pid_z(pid_input_z))
        return pid_tuple

    def set_x(self, value):
        self.setpoint_x = value
        self.pid_x = PID(self.kp, self.ki, self.kd, self.setpoint_x)

    def set_y(self, value):
        self.setpoint_y = value
        self.pid_y = PID(self.kp, self.ki, self.kd, self.setpoint_y)

    def set_z(self, value):
        self.setpoint_z = value
        self.pid_z = PID(self.kp, self.ki, self.kd, self.setpoint_z)

    def set_invalue(self, value):
        self.invalue = value
