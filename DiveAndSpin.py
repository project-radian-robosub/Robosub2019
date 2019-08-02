import time

import Control

ctr = Control

killed = True

target = 93


def get_killed():
    return killed


def set_killed(val):
    nonlocal killed
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

    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    try:
        ctr.imu.set_z(target)
        ctr.pressure.set_tar(1080)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while ctr.pressure.get_val(1070) and not killed:
            drive()

        ctr.imu.set_z(ctr.change_heading(target, 120))
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while timer2 - timer1 < 3 and not killed:
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(target, 240))
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while timer2 - timer1 < 3 and not killed:
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(target)
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while timer2 - timer1 < 3 and not killed:
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(target, 120))
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while ctr.imu.get_angles()[2] < 120 and not killed:
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(ctr.change_heading(target, 240))
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while ctr.imu.get_angles()[2] < 240 and not killed:
            drive()
            timer2 = time.perf_counter()

        ctr.imu.set_z(target)
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while timer2 - timer1 < 7 and not killed:
            drive()
            timer2 = time.perf_counter()

        ctr.pressure.set_tar(1060)
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while timer2 - timer1 < 3 and not killed:
            drive()
            timer2 = time.perf_counter()

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
