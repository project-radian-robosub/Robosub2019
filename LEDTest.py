import time

import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)
time.sleep(5)
GPIO.cleanup()
time.sleep(5)
