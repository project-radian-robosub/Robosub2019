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
        # ctr.imu.set_z(50)
        ctr.pressure.set_tar(1070)
        timer1 = time.perf_counter()
        timer2 = time.perf_counter()
        while not killed and timer2 - timer1 < 6:
            ctr.set_imu_powers()
            # ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)
            timer2 = time.perf_counter()
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
