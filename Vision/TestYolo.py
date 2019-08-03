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
    'annotation': '/TrainingData/NewAnnotations',
    'dataset': '/TrainingData/Images',
    'gpu': 1.0
}

tfnet = TFNet(options)
tfnet.train()
tfnet.savepb()

