import cv2
from darkflow.net.build import TFNet
import time


class Vision:

    def __init__(self, cam_num):
        self.options = {
            'model': 'cfg/yolov2-tiny-custom.cfg',
            'load': -500,
            'threshold': 0.50,
            'gpu': 0.0
        }

        self.results = 0
        self.stime = time.time()
        self.tl = (0, 0)
        self.br = (0, 0)
        self.label = []
        self.tfnet = TFNet(self.options)
        self.tfnet.load_from_ckpt()
        self.boxes_dict = {}
        self.capture = cv2.VideoCapture(cam_num)
        self.colors = [tuple('0, 225, 0'), tuple('255, 0, 0')]
        self.ret, self.frame = self.capture.read()

    def vision_generator(self, show=False):
        while True:
            ret, frame = self.capture.read()
            if ret:
                results = self.tfnet.return_predict(frame)
                for color, result in zip(self.colors, results):
                    label = result['label']
                    tl = (result['topleft']['x'], result['topleft']['y'])
                    br = (result['bottomright']['x'], result['bottomright']['y'])
                    coord = tuple(tl, br)
                    self.boxes_dict.append({label, coord})
                    if show:
                        frame = cv2.rectangle(frame, tl, br, color, 7)
                        frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
                if show:
                    cv2.imshow('frame', frame)
                    print('FPS {:.1f}'.format(1 / (time.time() - self.stime)))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                self.capture.release()
                cv2.destroyAllWindows()
                break
            yield self.boxes_dict

    def get_frame(self):
        if (time.time()-self.stime) >= 0.50:
            self._vision_generator()
            self.stime = time.time()
        else:
            print('Not Ready')


if __name__ == '__main__':
    v = Vision(0)
    time.sleep(40)
    while True:
        v.vision_generator(True)
