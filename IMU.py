from simple_pid import PID
import board
import busio
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

kp = 1
ki = 0
kd = 0

pid_euler_x = PID(kp, ki, kd, setpoint=0, output_limits=[-180, 180])
pid_euler_y = PID(kp, ki, kd, setpoint=0, output_limits=[-180, 180])
pid_euler_z = PID(kp, ki, kd, setpoint=0, output_limits=[-180, 180])


def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def recenter(imu_val):
    if imu_val > 180:
        imu_val = imu_val - 360
    return imu_val


imu_pid_val_x = pid_euler_x(recenter(sensor.euler[0]))
imu_pid_val_y = pid_euler_y(recenter(sensor.euler[1]))
imu_pid_val_z = pid_euler_z(recenter(sensor.euler[2]))

power_x_rotation = int(remap(imu_pid_val_x, -180, 180, 0, 100))
power_y_rotation = int(remap(imu_pid_val_y, -180, 180, 0, 100))
power_z_rotation = int(remap(imu_pid_val_z, -180, 180, 0, 100))
