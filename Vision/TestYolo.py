import matplotlib.pyplot as plt
import numpy as np
from darkflow.net.build import TFNet
import cv2

options = {
    'model': 'cfg/yolo-custom.cfg',
    'load': 'bin/yolo.weights',
    'batch': 8,
    'epoch': 100,
    'train': True,
    'annotation': '/home/stewe951/Documents/Robosub2019/TrainingData/Annotations',
    'dataset': '/home/stewe951/Documents/Robosub2019/TrainingData/Images'
}

tfnet = TFNet(options)
tfnet.train()
tfnet.savepb()

