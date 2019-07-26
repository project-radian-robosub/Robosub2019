import Control
import time

ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

try:
    while ctr.pressure.get_val() < 980:  # dive
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 20:  # forward
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(75, 0, 0, 0, 0, 75)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 3:  # stop
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    ctr.imu.set_z(180)  # set new target

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 15:  # allow time to reach new target
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 20:  # go forward
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(75, 0, 0, 0, 0, 75)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    ctr.stop_all()

    exit(1)

except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
