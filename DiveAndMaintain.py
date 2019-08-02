import time

import Control

ctr = Control

killed = True

while killed:

    ctr.MotorMovement.wait_for_arduino()

    killed = False

    ctr.stop_all()

    try:
        target = 93
        ctr.imu.set_z(target)
        # ctr.pressure.set_tar(1100)
        while not killed:
            ctr.set_imu_powers()
            # ctr.set_pressure_powers()
            ctr.set_move_powers(0, 0, 0, 0, 0, 0)
            ctr.set_motor_powers()
            print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)
            timer2 = time.perf_counter()
            '''
            new_tar = target + ctr.calculate_mag_error()
            if new_tar > 360:
                new_tar -= 360
            elif new_tar < 0:
                new_tar += 360
            ctr.imu.set_z(new_tar)
            '''
            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

    except KeyboardInterrupt:
        ctr.stop_all()
        print("end")

    finally:
        ctr.stop_all()
        print("end")
