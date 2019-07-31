import time

from Vision import VisionV2

import Control

ctr = Control

v1 = VisionV2.vision_generator(0, True)

center_x_px = 320
center_y_px = 240

killed = True


def find_proportion(prop, value):
    new = prop * value
    return new


while killed:

    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    try:
        ctr.imu.set_z(330)
        ctr.pressure.set_tar(1100)

        while not killed and ctr.pressure.get_val() < 1080:
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while not killed and (len(v1.__next__()) < 3 or v1.__next__() == "null") and timer2 - timer1 < 40:  # go forward until see gate
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(75, 0, 0, 0, 0, 75)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while not killed and timer2 - timer1 < 4:  # stop
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while not killed and len(v1.__next__()) == 3 and timer2 - timer1 < 4:  # approach gate
            box_dictionary = v1.__next__()
            x1, y1 = box_dictionary[0]['tl']
            x2, y2 = box_dictionary[2]['br']
            px_tar_x = (x1 + x2) / 2
            px_tar_y = (y1 + y2) / 2
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
