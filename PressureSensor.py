import ms5837
from simple_pid import PID

p_sensor = ms5837.MS5837_30BA()


class Pressure:
    kp = 0
    ki = 0
    kd = 0
    setpoint = 0

    def __init__(self, kp, ki, kd, setpoint=0):
        self.pid_pressure = PID(kp, ki, kd, setpoint, output_limits=[50, 50])
        self.setpoint = setpoint
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def get_pid(self):
        p_sensor.read()
        pid_val = self.pid_pressure(p_sensor.pressure())
        return pid_val

    def set_tar(self, val):
        self.setpoint = val
        self.pid_pressure = PID(self.kp, self.ki, self.kd, self.setpoint)
