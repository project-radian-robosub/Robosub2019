import time

from Vision.BackgroundSubtractor import VisionV3

v1 = VisionV3(0)
gen = v1.vision_generator(True)

while True:
    print(len(gen.__next__()))
    time.sleep(.1)
