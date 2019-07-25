import time
import Control

while True:
    print(Control.imu.get_acc())
    time.sleep(0.01)
