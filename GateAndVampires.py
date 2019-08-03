import time

from Vision.BackgroundSubtractor import VisionV3

import Control

v1 = VisionV3(0)
gen = v1.vision_generator(True)
ctr = Control
killed = True
gate_tar = 220
p_tar = 1080
p_thresh = p_tar - 10
depth_increment = 2


def get_killed():
    return killed


def set_killed(val):
    global killed
    killed = val


def drive(m2=0, m3=0, m4=0, m5=0, m6=0, m7=0):
    ctr.set_imu_powers()
    ctr.set_pressure_powers()
    ctr.set_move_powers(m2, m3, m4, m5, m6, m7)
    ctr.set_motor_powers()
    print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)
    if ctr.MotorMovement.check_reset():
        set_killed(True)
        print('KILLED')


while killed:

    ctr.MotorMovement.wait_for_initialization()

    killed = False

    ctr.stop_all()

    time.sleep(0.1)

    try:
        ctr.imu.set_z(gate_tar)
        ctr.pressure.set_tar(p_tar)
        while ctr.pressure.get_val() < p_thresh and not killed:
            drive()

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        gate_flag = False
        seen = False
        while gate_flag is False and not killed:  # forward
            if not gen.__next__() is None and not seen:
                timer1 = time.perf_counter()
                timer2 = time.perf_counter()
                seen = True
            if gen.__next__() is None and seen:
                seen = False
            if timer2 - timer1 > 0.2 and seen is True:
                gate_flag = True
            drive(m2=75, m7=75)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        seen = True
        timer3 = time.perf_counter()
        timer4 = time.perf_counter()
        while gate_flag is True and timer4 - timer3 < 40 and not killed:  # forward
            if gen.__next__() is None and seen:
                timer1 = time.perf_counter()
                timer2 = time.perf_counter()
                seen = False
            if not gen.__next__() is None and not seen:
                seen = True
            if timer2 - timer1 > 0.2 and seen is True:
                gate_flag = False
            tl, br = gen.__next__()
            x = (tl[0] + br[0]) / 2
            y = (tl[1] + br[1]) / 2
            x_pow = 320 - x
            y_pow = 240 - y
            if x_pow > 100:
                x_pow = 100
            elif x_pow < -100:
                x_pow = -100
            if y_pow > 100:
                y_pow = 100
            elif y_pow < -100:
                y_pow = -100
            drive(m2=75, m3=x_pow * 1.5, m6=x_pow * 1.5, m7=75)
            timer4 = time.perf_counter()

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 3 and not killed:  # stop
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(gate_tar, 120))
        while timer2 - timer1 < 6 and not killed:  # spin
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(gate_tar, 240))
        while timer2 - timer1 < 9 and not killed:  # spin
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(gate_tar)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 3 and not killed:  # spin
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(gate_tar, 120))
        while timer2 - timer1 < 6 and not killed:  # spin
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(gate_tar, 240))
        while timer2 - timer1 < 9 and not killed:  # spin
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(gate_tar)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 4 and not killed:  # stabilize
            drive()
            timer2 = time.perf_counter()

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 3 and not killed:
            drive(m2=75, m7=75)
            timer2 = time.perf_counter()

        p_tar = 1270
        ctr.pressure.set_tar(p_tar)

        while ctr.pressure.get_val() < p_thresh and not killed:  # dive
            drive()
            timer2 = time.perf_counter()

        while gate_flag is False and not killed:  # forward
            if not gen.__next__() is None and not seen:
                timer1 = time.perf_counter()
                timer2 = time.perf_counter()
                seen = True
            if gen.__next__() is None and seen:
                seen = False
            if timer2 - timer1 > 0.2 and seen is True:
                gate_flag = True
            drive(m2=75, m7=75)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        seen = True
        timer3 = time.perf_counter()
        timer4 = time.perf_counter()
        while gate_flag is True and timer4 - timer3 < 20 and not killed:  # forward
            if gen.__next__() is None and seen:
                timer1 = time.perf_counter()
                timer2 = time.perf_counter()
                seen = False
            if not gen.__next__() is None and not seen:
                seen = True
            if timer2 - timer1 > 0.2 and seen is True:
                gate_flag = False
            tl, br = gen.__next__()
            x = br[0]
            y = (tl[1] + br[1]) / 2
            x_pow = 320 - x
            y_pow = 240 - y
            if x_pow > 100:
                x_pow = 100
            elif x_pow < -100:
                x_pow = -100
            if y_pow > 100:
                y_pow = 100
            elif y_pow < -100:
                y_pow = -100
            if y_pow > 0:
                p_tar += depth_increment
                ctr.pressure.set_tar(p_tar)
            if y_pow < 0:
                p_tar -= depth_increment
                ctr.pressure.set_tar(p_tar)
            drive(m2=75, m3=x_pow * 1.5, m6=x_pow * 1.5, m7=75)
            timer4 = time.perf_counter()

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
