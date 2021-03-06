import time

import Control

ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

try:
    ctr.pressure.set_tar(1000)
    while True:
        # ctr.set_acc_powers()
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)


except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
