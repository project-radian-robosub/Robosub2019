import time

import Control

ctr = Control
killed = True


while killed:
    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    time.sleep(0.1)

    try:
        ctr.pressure.set_tar(1100)
        while ctr.pressure.get_val() < 1080 and not killed:
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

        while timer2 - timer1 < 10 and not killed:  # forward
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

        while timer2 - timer1 < 4 and not killed:  # stop
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(90)
        while timer2 - timer1 < 2 and not killed:  # stop
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')
        while ctr.imu.get_angles()[2] < 90 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(180)
        while ctr.imu.get_angles()[2] < 180 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(270)
        while ctr.imu.get_angles()[2] < 270 and not killed:  # spin
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        ctr.imu.set_z(0)
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 10 and not killed:  # stop
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
