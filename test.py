import MotorMoveTest
import time

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
motor_strings = ["050", "050", "050", "050", "050", "050"]
all_motors_stop = "050050050050050050"
pwr = 20


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

    m2_corou = MotorMoveTest.motor_coroutine(0)
    m3_corou = MotorMoveTest.motor_coroutine(1)
    m4_corou = MotorMoveTest.motor_coroutine(2)
    m5_corou = MotorMoveTest.motor_coroutine(3)
    m6_corou = MotorMoveTest.motor_coroutine(4)
    m7_corou = MotorMoveTest.motor_coroutine(5)

    print(all_motors_stop)

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
    print(all_motors_stop)
