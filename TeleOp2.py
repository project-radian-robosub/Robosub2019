from serial import Serial
import MotorMovement
import cv2
import os
import IMU
import PressureSensor

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
motor_strings = ["050", "050", "050", "050", "050", "050"]
all_motors_stop = "050050050050050050"
pwr = 20

ser = Serial("/dev/ttyACM0", 9600)

imu = IMU.IMU()
pressure = PressureSensor.Pressure()


def wait_for_arduino():
    msg = ""
    while msg.find("ready") == -1:
        if ser.inWaiting() > 0:
            c = ser.read()
            msg += c.decode('utf-8')
            print("Arduino" + msg)


def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def forward_backward(power):
    m2_corou.send(power)
    m3_corou.send(0)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(0)
    m7_corou.send(power)


def left_right(power):
    m2_corou.send(0)
    m3_corou.send(power)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(power)
    m7_corou.send(0)


def up_down(power):
    m2_corou.send(0)
    m3_corou.send(0)
    m4_corou.send(power)
    m5_corou.send(power)
    m6_corou.send(0)
    m7_corou.send(0)


def roll(power):
    m2_corou.send(0)
    m3_corou.send(power)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(-power)
    m7_corou.send(0)


def pitch(power):
    m2_corou.send(0)
    m3_corou.send(0)
    m4_corou.send(-power)
    m5_corou.send(power)
    m6_corou.send(0)
    m7_corou.send(0)


def yaw(power):
    m2_corou.send(power)
    m3_corou.send(0)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(0)
    m7_corou.send(-power)


def stop():
    m2_corou.send(0)
    m3_corou.send(0)
    m4_corou.send(0)
    m5_corou.send(0)
    m6_corou.send(0)
    m7_corou.send(0)


try:
    wait_for_arduino()

    m2_corou = MotorMovement.motor_coroutine(0)
    m3_corou = MotorMovement.motor_coroutine(1)
    m4_corou = MotorMovement.motor_coroutine(2)
    m5_corou = MotorMovement.motor_coroutine(3)
    m6_corou = MotorMovement.motor_coroutine(4)
    m7_corou = MotorMovement.motor_coroutine(5)

    ser.write(all_motors_stop.encode())

    text_file = open(r"/home/%s/TeleOpData/TeleOpSensorData/Data.txt", "w")

    while True:

        if cv2.waitKey(1) & 0xFF == ord('z'):
            break

        if cv2.waitKey(1) & 0xFF == ord('w'):
            forward_backward(pwr)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            forward_backward(-pwr)

        if cv2.waitKey(1) & 0xFF == ord('a'):
            left_right(-pwr)

        if cv2.waitKey(1) & 0xFF == ord('d'):
            left_right(pwr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            up_down(-pwr)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            up_down(pwr)

        if cv2.waitKey(1) & 0xFF == ord('i'):
            pitch(pwr)

        if cv2.waitKey(1) & 0xFF == ord('k'):
            pitch(-pwr)

        if cv2.waitKey(1) & 0xFF == ord('j'):
            yaw(-pwr)

        if cv2.waitKey(1) & 0xFF == ord('l'):
            yaw(pwr)

        if cv2.waitKey(1) & 0xFF == ord('u'):
            roll(-pwr)

        if cv2.waitKey(1) & 0xFF == ord('o'):
            roll(pwr)

        if cv2.waitKey(1) & 0xFF == ord('f'):
            stop()

        text_file.write(str(int(pressure.get_val())), str(int(imu.get_angles())))


finally:
    camera.release()
    cv2.destroyAllWindows()
    targets = [0, 0, 0, 0, 0, 0]
    stop()
