import os

import cv2

import Control

ctr = Control


def count_files(path):
    path, dirs, files = next(os.walk(path))
    return len(files)


path = '/home/projectradian/AndrewGit/Robosub2019/Vision/TrainingData/Images'
count = count_files(path) + 1

camera = cv2.VideoCapture(1)
if camera.read() == (False, None):
    camera = cv2.VideoCapture(0)


while True:
    return_value, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image', image)

    # Take a screenshot if 's' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        status = cv2.imwrite(os.path.join(path, '%d.jpg' % count), image)
        count += 1
        print(status)

    # Exit if escape is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    print(ctr.pressure.get_val())


camera.release()
cv2.destroyAllWindows()