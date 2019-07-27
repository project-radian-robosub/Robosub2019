import Control
import sys, termios, tty
import time


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

x = 0
y = 0
depth = 990
x_rot = 0
y_rot = 0
z_rot = 0

try:
    while True:
        char = getch()

        if char == "z":
            break

        if char == "w":
            y += 1
            time.sleep(.001)

        if char == "s":
            y -= 1
            time.sleep(.001)

        if char == "a":
            x -= 1
            time.sleep(.001)

        if char == "d":
            x += 1
            time.sleep(.001)

        if char == "q":
            depth -= 1
            time.sleep(.001)

        if char == "e":
            depth += 1
            time.sleep(.001)

        if char == "i":
            x_rot += 1
            time.sleep(.001)

        if char == "k":
            x_rot -= 1
            time.sleep(.001)

        if char == "j":
            z_rot -= 1
            time.sleep(.001)

        if char == "l":
            z_rot += 1
            time.sleep(.001)

        if char == "u":
            y_rot -= 1
            time.sleep(.001)

        if char == "o":
            y_rot += 1
            time.sleep(.001)

        if char == "r":
            x = 0
            y = 0
            depth = 990
            x_rot = 0
            y_rot = 0
            z_rot = 0

        if char == "f":
            ctr.stop_all()

        ctr.imu.set_x(x_rot)
        ctr.imu.set_y(y_rot)
        ctr.imu.set_z(z_rot)
        ctr.pressure.set_tar(depth)
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(y, x, 0, 0, x, y)
        ctr.set_motor_powers()

except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
