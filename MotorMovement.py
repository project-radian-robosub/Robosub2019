import os
import time

from serial import Serial

ard_port = -1
ard_path = '/dev/ttyACM0'
if os.path.exists('/dev/ttyACM0'):
    ser = Serial('/dev/ttyACM0', 9600)
    ard_path = '/dev/ttyACM0'
    print('/dev/ttyACM0')

elif os.path.exists('/dev/ttyACM1'):
    ser = Serial('/dev/ttyACM1', 9600)
    ard_path = '/dev/ttyACM1'
    print('/dev/ttyACM1')

elif os.path.exists('/dev/ttyACM2'):
    ser = Serial('/dev/ttyACM2', 9600)
    ard_path = '/dev/ttyACM2'
    print('/dev/ttyACM2')

else:
    print('SERIAL FAILURE')

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
motor_strings = ["050", "050", "050", "050", "050", "050"]
current_vals = [0, 0, 0, 0, 0, 0]

reverse = -1


def get_ard_path():
    return ard_path


def set_ard_path(path):
    global ard_path
    ard_path = path


def wait_for_arduino():
    global ard_path
    global ser

    while os.path.exists(get_ard_path()):
        print('has not broken yet')
        time.sleep(.1)
        if not os.path.exists(get_ard_path()):
            break

    if os.path.exists('/dev/ttyACM0'):
        ser = Serial('/dev/ttyACM0', 9600)
        ard_path = '/dev/ttyACM0'
        print('/dev/ttyACM0')

    elif os.path.exists('/dev/ttyACM1'):
        ser = Serial('/dev/ttyACM1', 9600)
        ard_path = '/dev/ttyACM1'
        print('/dev/ttyACM1')

    elif os.path.exists('/dev/ttyACM2'):
        ser = Serial('/dev/ttyACM2', 9600)
        ard_path = '/dev/ttyACM2'
        print('/dev/ttyACM2')

    msg = ""
    while msg.find("ready") == -1:
        if ser.inWaiting() > 0:
            c = ser.read()
            msg += c.decode('utf-8')
    print("Arduino" + msg)


def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        g.__next__()
        return g
    return start


def vals_to_serial(vals):
    for i in range(len(vals)):
        motor_strings[i] = str(int(remap(vals[i], -100, 100, 0, 100)))
        while len(motor_strings[i]) < 3:
            motor_strings[i] = '0' + motor_strings[i]
    write_all = ''
    for i in motor_strings:
        write_all += i

    ser.write(write_all.encode())


def motor_generator():
    try:
        while True:
            for motor_num in range(6):
                if current_vals[motor_num] < targets[motor_num]:

                    current_vals[motor_num] += 5

                if current_vals[motor_num] > targets[motor_num]:

                    current_vals[motor_num] -= 5

            vals_to_serial(current_vals)

            time.sleep(.01)

            yield

    except GeneratorExit:
        print("motor co-routine closed")
