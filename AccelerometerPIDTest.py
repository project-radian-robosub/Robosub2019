import Control
import time

ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

try:
    ctr.acc_pid_x_enable(False, 15, 0, 0)
    ctr.acc_pid_y_enable(False, 15, 0, 0)
    ctr.imu.set_z(180)
    while True:
        ctr.set_acc_powers()
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        print(ctr.imu.get_angles(), ctr.imu.get_acc(), ctr.pressure.get_val(), ctr.MotorMovement.targets)


except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
