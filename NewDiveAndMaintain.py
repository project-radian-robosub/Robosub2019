import time

import Control

ctr = Control

killed = True


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

    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    try:
        target = 0
        ctr.imu.set_z(target)
        ctr.pressure.set_tar(1080)
        while not killed:
            drive()
            timer2 = time.perf_counter()
            '''
            new_tar = target + ctr.calculate_mag_error()
            if new_tar > 360:
                new_tar -= 360
            elif new_tar < 0:
                new_tar += 360
            ctr.imu.set_z(new_tar)
            '''

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
