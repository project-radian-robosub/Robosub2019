import time

import Control

ctr = Control

killed = True

target = 220

while killed:

    ctr.MotorMovement.wait_for_initialization()

    killed = False

    ctr.stop_all()

    try:
        ctr.imu.set_z(target)
        ctr.pressure.set_tar(1080)
        while not killed:
            ctr.set_imu_powers()
            # ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')
            timer2 = time.perf_counter()

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
