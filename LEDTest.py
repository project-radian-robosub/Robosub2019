import time

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT)
time.sleep(1)
while True:
    GPIO.output(21, GPIO.HIGH)
