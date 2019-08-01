import time

from Vision.BackgroundSubtractor import VisionV3

v1 = VisionV3.vision_generator(0, True)

while True:
    print(len(v1.__next__()))
    time.sleep(.1)
