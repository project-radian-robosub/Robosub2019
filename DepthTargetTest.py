import Control
import time

ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

try:
    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 5:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)

    ctr.pressure.set_tar(970)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 15:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)

    ctr.pressure.set_tar(100)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 15:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)


except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
