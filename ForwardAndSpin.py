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
        # ctr.imu.set_z(228)
        ctr.pressure.set_tar(1085)
        while ctr.pressure.get_val() < 1075 and not killed:
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
        ctr.imu.set_y(160)
        while timer2 - timer1 < 1 and not killed:
            ctr.set_imu_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')
            timer2 = time.perf_counter()

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        # ctr.imu.set_x(90)
        while timer2 - timer1 < 3 and not killed:
            ctr.set_imu_powers()
            ctr.set_move_powers(0, 75, 0, 0, -75, 0)
            ctr.set_motor_powers()
            if ctr.MotorMovement.imu.sensor.calibration_status[3] > 2:
                ctr.MotorMovement.GPIO.output(40, ctr.MotorMovement.GPIO.HIGH)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')
            timer2 = time.perf_counter()


        ctr.imu.set_y(0)
        ctr.imu.set_z(228)

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while timer2 - timer1 < 10 and not killed:  # forward
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            timer2 = time.perf_counter()
            print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)
            if ctr.MotorMovement.imu.sensor.calibration_status[3] > 2:
                ctr.MotorMovement.GPIO.output(40, ctr.MotorMovement.GPIO.HIGH)
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
            if ctr.MotorMovement.imu.sensor.calibration_status[3] > 2:
                ctr.MotorMovement.GPIO.output(40, ctr.MotorMovement.GPIO.HIGH)
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

        # ctr.imu.set_z(318)
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

        ctr.imu.set_z(0)
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

        ctr.imu.set_z(138)
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

        ctr.imu.set_z(228)
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
