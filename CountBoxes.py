import time

from Vision import VisionV2

v1 = VisionV2.vision_generator(0, True)

while True:
    print(len(v1.__next__()))
    time.sleep(.1)
