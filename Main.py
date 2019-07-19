from serial import Serial
import IMU
import time

ser = Serial("/dev/ttyAM0", 9600)

imu = IMU

motor_values = [0, 0, 0, 0, 0, 0]
motor_values_str = ['050', '050', '050', '050', '050', '050']
all_motor_values = '050050050050050050'


def wait_for_arduino():
    msg = ""
    while msg.find("ready") == -1:
        if ser.inWaiting() > 0:
            c = ser.read()
            msg += c.decode('utf-8')
            print(msg)


wait_for_arduino()

imu.sensor.reset()

ser.write(all_motor_values.encode())

timer1 = time.perf_counter()
timer2 = time.perf_counter()

while timer2 - timer1 < 30:
    all_motor_values = ""

    motor_values[0] = imu.power_z_rotation
    motor_values[1] = imu.power_y_rotation
    motor_values[2] = 100 - imu.power_x_rotation
    motor_values[3] = imu.power_x_rotation
    motor_values[4] = 100 - imu.power_y_rotation
    motor_values[5] = 100 - imu.power_z_rotation

    for i in motor_values:
        motor_values_str[i] = str(motor_values[i])

        while len(motor_values_str[i]) < 3:
            motor_values_str[i] = '0' + motor_values_str[i]

        all_motor_values += motor_values_str[i]

    ser.write(all_motor_values.encode())
    timer2 = time.perf_counter()


all_motor_values = '050050050050050050'
ser.write(all_motor_values.encode())
