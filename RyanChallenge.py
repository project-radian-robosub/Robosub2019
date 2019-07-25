import Control
import time

ctr = Control

ctr.MotorMovement.wait_for_arduino()

ctr.stop_all()

time.sleep(0.1)

try:
    while ctr.pressure.get_val() < 980:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 5:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(50, 0, 0, 0, 0, 50)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 3:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    ctr.imu.set_z(180)

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 10:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(0, 0, 0, 0, 0, 0)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()

    timer1 = time.perf_counter()
    timer2 = time.perf_counter()

    while timer2 - timer1 < 5:
        ctr.set_imu_powers()
        ctr.set_pressure_powers()
        ctr.set_move_powers(50, 0, 0, 0, 0, 50)
        ctr.set_motor_powers()
        timer2 = time.perf_counter()
        print(ctr.imu.get_angles(), ctr.pressure.get_val(), ctr.MotorMovement.targets)

    ctr.stop_all()

except KeyboardInterrupt:
    ctr.stop_all()
    print("end")

finally:
    ctr.stop_all()
    print("end")
