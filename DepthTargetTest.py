import Control
import time

ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

try:
    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 10:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.pressure.get_val())

    ctr.pressure.set_tar(990)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 15:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.pressure.get_val())

    ctr.pressure.set_tar(840)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 15:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.pressure.get_val())


except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
