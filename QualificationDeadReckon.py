import time

import Control

ctr = Control
timer1 = time.perf_counter()
timer2 = time.perf_counter()
# ctr.MotorMovement.wait_for_arduino()
while timer2 - timer1 < 60:
    print(timer2 - timer1)
    time.sleep(.1)
    timer2 = time.perf_counter()

ctr.stop_all()

time.sleep(0.1)

try:
    ctr.pressure.set_tar(1140)
    while ctr.pressure.get_val() < 1130:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        print(ctr.imu.get_angles(), ctr.imu.get_angle_pid(), ctr.imu.center_z)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 45:  # forward
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(75, 0, 0, 0, 0, 75)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 4:  # stop
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)


except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
