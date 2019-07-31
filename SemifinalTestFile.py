import time

import Control

ctr = Control

killed = True

while killed:

    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    try:
        ctr.imu.set_z(325)
        ctr.pressure.set_tar(1100)

        while not killed and ctr.pressure.get_val() < 1080:
            ctr.set_imu_powers()
            ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)
            timer2 = time.perf_counter()
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

        timer1 = time.perf_counter()
        timer2 = time.perf_counter()

        while not killed and timer2 - timer1 < 45:  # forward
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

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
