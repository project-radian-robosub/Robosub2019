import os
import time

import cv2

import Control
import MotorMovement

targets = [0, 0, 0, 0, 0, 0]  # forward-backward, left-right, up-down, roll, pitch, yaw
max_pwr = 60
pwr = 20

killed = False

def remap(x, b1, b2, v1, v2):
    prop = (x - b1) / (b2 - b1)
    new_prop = prop * (v2 - v1)
    new = v1 + new_prop
    return new


def count_files(path):
    path, dirs, files = next(os.walk(path))
    return len(files)


path = '/home/projectradian/AndrewGit/Robosub2019/Vision/TrainingData/Images'
count = count_files(path) + 1

camera = cv2.VideoCapture(1)
if camera.read() == (False, None):
    camera = cv2.VideoCapture(0)

ctr = Control

while killed:
    try:
        MotorMovement.wait_for_arduino()

        killed = False

        ctr.stop_all()

        time.sleep(.1)
        while not killed:
            return_value, image = camera.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow('image', image)

            # Take a screenshot if 'g' is pressed
            if cv2.waitKey(1) & 0xFF == ord('g'):
                status = cv2.imwrite(os.path.join(path, '%d.jpg' % count), image)
                count += 1
                print(status)

            if cv2.waitKey(1) & 0xFF == ord('z'):
                break

            if cv2.waitKey(5) & 0xFF == ord('w'):
                if targets[0] < max_pwr:
                    targets[0] += pwr
                if targets[5] < max_pwr:
                    targets[5] += pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                if targets[0] > -max_pwr:
                    targets[0] -= pwr
                if targets[5] > -max_pwr:
                    targets[5] -= pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('a'):
                if targets[1] > -max_pwr:
                    targets[1] -= pwr
                if targets[4] > -max_pwr:
                    targets[4] -= pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('d'):
                if targets[1] < max_pwr:
                    targets[1] += pwr
                if targets[4] < max_pwr:
                    targets[4] += pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if targets[2] > -max_pwr:
                    targets[2] -= pwr
                if targets[3] > -max_pwr:
                    targets[3] -= pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('e'):
                if targets[2] < max_pwr:
                    targets[2] += pwr
                if targets[3] < max_pwr:
                    targets[3] += pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('i'):
                if targets[2] < max_pwr:
                    targets[2] += pwr
                if targets[3] > -max_pwr:
                    targets[3] -= pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('k'):
                if targets[2] > -max_pwr:
                    targets[2] -= pwr
                if targets[3] < max_pwr:
                    targets[3] += pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('j'):
                if targets[0] < max_pwr:
                    targets[0] += pwr
                if targets[5] > -max_pwr:
                    targets[5] -= pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('l'):
                if targets[0] > -max_pwr:
                    targets[0] -= pwr
                if targets[5] < max_pwr:
                    targets[5] += pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('u'):
                if targets[1] > -max_pwr:
                    targets[1] -= pwr
                if targets[4] < max_pwr:
                    targets[4] += pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('o'):
                if targets[1] < max_pwr:
                    targets[1] += pwr
                if targets[4] > -max_pwr:
                    targets[4] -= pwr
                time.sleep(.01)

            if cv2.waitKey(1) & 0xFF == ord('f'):
                ctr.stop_all()
                for i in range(len(targets)):
                    targets[i] = 0

            if ctr.MotorMovement.check_reset():
                killed = True
                print('KILLED')

            print(ctr.pressure.get_val())
            # ctr.set_acc_powers()
            ctr.set_imu_powers()
            # ctr.set_pressure_powers()
            ctr.set_move_powers(targets[0], targets[1], targets[2], targets[3], targets[4], targets[5])
            ctr.set_motor_powers()

    finally:
        targets = [0, 0, 0, 0, 0, 0]
        ctr.stop_all()
        camera.release()
        cv2.destroyAllWindows()

