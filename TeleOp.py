from serial import Serial
import time

ser = Serial("/dev/usb/bin/001/006", 9600)

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
motor_strings = ["050", "050", "050", "050", "050", "050"]
all_motors_stop = "050050050050050050"
pwr = 50


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


def motor_coroutine(motor_num):
    try:
        while True:
            target = (yield)
            while targets[motor_num] < target:
                targets[motor_num] += 5
                mot_str = str(int(remap(targets[motor_num], -100, 100, 0, 100)))
                while len(mot_str) < 3:
                    mot_str = "0" + mot_str
                motor_strings[motor_num] = mot_str
                write_all_motors = ""
                for i in motor_strings:
                    write_all_motors += i
                ser.write(write_all_motors)
                print(write_all_motors)
                time.sleep(.01)
            while targets[motor_num] > target:
                targets[motor_num] -= 5
                mot_str = str(int(remap(targets[motor_num], -100, 100, 0, 100)))
                while len(mot_str) < 3:
                    mot_str = "0" + mot_str
                motor_strings[motor_num] = mot_str
                write_all_motors = ""
                for i in motor_strings:
                    write_all_motors += i
                ser.write(write_all_motors)
                print(motor_strings)
                time.sleep(.01)

    except GeneratorExit:
        print("motor co-routine closed")


def forward_backward(power):
    m2_corou.send(power)
    m3_corou.send(0)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(0)
    m7_corou.send(power)


def left_right(power):
    m2_corou.send(0)
    m3_corou.send(power)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(power)
    m7_corou.send(0)


def up_down(power):
    m2_corou.send(0)
    m3_corou.send(0)
    m4_corou.send(power)
    m5_corou.send(power)
    m6_corou.send(0)
    m7_corou.send(0)


def roll(power):
    m2_corou.send(0)
    m3_corou.send(power)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(-power)
    m7_corou.send(0)


def pitch(power):
    m2_corou.send(0)
    m3_corou.send(0)
    m4_corou.send(-power)
    m5_corou.send(power)
    m6_corou.send(0)
    m7_corou.send(0)


def yaw(power):
    m2_corou.send(power)
    m3_corou.send(0)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(0)
    m7_corou.send(-power)


def stop():
    m2_corou.send(0)
    m3_corou.send(0)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(0)
    m7_corou.send(0)

try:
    wait_for_arduino()

    m2_corou = motor_coroutine(0)
    m3_corou = motor_coroutine(1)
    m4_corou = motor_coroutine(2)
    m5_corou = motor_coroutine(3)
    m6_corou = motor_coroutine(4)
    m7_corou = motor_coroutine(5)
    m2_corou.__next__()
    m3_corou.__next__()
    m4_corou.__next__()
    m5_corou.__next__()
    m6_corou.__next__()
    m7_corou.__next__()

    ser.write(all_motors_stop)

    while True:
        char = input("?")

        if char == "z":
            break

        if char == "w":
            forward_backward(pwr)

        if char == "s":
            forward_backward(-pwr)

        if char == "a":
            left_right(-pwr)

        if char == "d":
            left_right(pwr)

        if char == "q":
            up_down(-pwr)

        if char == "e":
            up_down(pwr)

        if char == "i":
            pitch(pwr)

        if char == "k":
            pitch(-pwr)

        if char == "j":
            yaw(-pwr)

        if char == "l":
            yaw(pwr)

        if char == "u":
            roll(-pwr)

        if char == "o":
            roll(pwr)

        if char == "f":
            stop()

        print(targets)


finally:
    targets = [0, 0, 0, 0, 0, 0]
    ser.write(all_motors_stop)
