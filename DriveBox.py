import time

from Vision.BackgroundSubtractor import VisionV3

import Control

v1 = VisionV3(0)
gen = v1.vision_generator(True)
ctr = Control
killed = True
gate_tar = 93


while killed:
    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    time.sleep(0.1)

    try:
        ctr.imu.set_z(gate_tar)
        ctr.pressure.set_tar(1085)
        while ctr.pressure.get_val() < 1070 and not killed:
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
        seen = True
        while gate_flag is True and not killed:  # forward
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
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(75, x_pow * 1.5, 0, 0, x_pow * 1.5, 75)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 7 and not killed:
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

        while timer2 - timer1 < 3 and not killed:  # stop
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(ctr.change_heading(gate_tar, 120))
        while timer2 - timer1 < 6 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(ctr.change_heading(gate_tar, 240))
        while timer2 - timer1 < 9 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(gate_tar)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 3 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(ctr.change_heading(gate_tar, 120))
        while timer2 - timer1 < 6 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(ctr.change_heading(gate_tar, 240))
        while timer2 - timer1 < 9 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(gate_tar)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 4 and not killed:  # spin
            ctr.set_imu_powers()
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
