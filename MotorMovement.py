from serial import Serial
import time

ser = Serial("/dev/ttyACM0", 9600)

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
motor_strings = ["050", "050", "050", "050", "050", "050"]
current_vals = [0, 0, 0, 0, 0, 0]

reverse = -1


def wait_for_arduino():
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


def motor_generator():
    try:
        while True:
            for motor_num in range(6):
                if current_vals[motor_num] < targets[motor_num]:

                    current_vals[motor_num] += 5

                    mot_str = str(int(remap(current_vals[motor_num], -100, 100, 0, 100)))

                    while len(mot_str) < 3:
                        mot_str = "0" + mot_str

                    motor_strings[motor_num] = mot_str
                    write_all_motors = ""

                    for i in motor_strings:
                        write_all_motors += i

                    ser.write(write_all_motors.encode())

                if current_vals[motor_num] > targets[motor_num]:

                    current_vals[motor_num] -= 5

                    mot_str = str(int(remap(current_vals[motor_num], -100, 100, 0, 100)))

                    while len(mot_str) < 3:
                        mot_str = "0" + mot_str

                    motor_strings[motor_num] = mot_str
                    write_all_motors = ""

                    for i in motor_strings:
                        write_all_motors += i

                    ser.write(write_all_motors.encode())

            time.sleep(.01)

            yield

    except GeneratorExit:
        print("motor co-routine closed")
