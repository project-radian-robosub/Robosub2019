import time

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
time.sleep(1)
while True:
    GPIO.output(40, GPIO.HIGH)
