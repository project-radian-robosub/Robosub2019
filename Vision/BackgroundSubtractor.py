import numpy as np
import cv2
import time


class VisionV3:

    def __init__(self, cam_number):
        self.cap = cv2.VideoCapture(cam_number)

        self.width = 640
        self.height = 480

        self.cap.set(cv2.CAP_PROP_FPS, 15.0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def vision_generator(self, show=False):
        boxes = [None]

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()

        while True:
            success, img = self.get_cap().read()
            # print('justin')
            if success:
                blur = cv2.GaussianBlur(img, (5, 5), 10)
                fgmask = fgbg.apply(blur)
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

                _, contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                height, width, _ = img.shape
                min_x, min_y = width, height
                max_x = max_y = 0

                for i in range(len(contours)):


                    x, y, w, h = cv2.boundingRect(contours[i])

                    if w > 25 and h > 80:
                        '''
                        tl = (x, y)
                        br = (x + w, y + h)
                        '''

                        min_x, max_x = min(x, min_x), max(x + w, max_x)
                        min_y, max_y = min(y, min_y), max(y + h, max_y)

                        tl = (min_x, min_y)
                        br = (max_x, max_y)

                        # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 3)

                        box_ori = (tl, br)
                        # boxes.append(box_ori)

                        # rect = cv2.minAreaRect(contours[i])
                        # box = cv2.boxPoints(rect)
                        # box_d = np.int0(box)
                        # cv2.drawContours(img, [box_d], 0, (0, 255, 0), 3)
                        # cv2.drawContours(blur, contours[i], -1, (255, 0, 0))
                if show:
                    w, q = tuple(box_ori)
                    x1, y1 = w
                    x2, y2 = q

                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    print(box_ori)

                    cv2.imshow('Image', img)
                    cv2.imshow('contour', fgmask)

                yield box_ori
            yield

    def get_cap(self):
        return self.cap

    def set_cap(self, cam_num):
        self.cap = cam_num

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


if __name__ == '__main__':
    """
        options {
            arr[]
            arr[]
            tuple(0,0,0)
        }
    """

    v = VisionV3(1)
    print('Starting Loop')
    v_gen = v.vision_generator(True)

    while True:
        v_gen.__next__()
        # print('running')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    v.get_cap().release()
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()
