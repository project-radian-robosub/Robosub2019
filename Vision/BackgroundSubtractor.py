import numpy as np
import cv2


class VisionV3:

    def __init__(self, cam_number):
        self.cap = cv2.VideoCapture(cam_number)

        self.cap.set(cv2.CAP_PROP_FPS, 15.0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def vision_generator(self, show=False):
        boxes = ['null']

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgbg = cv2.createBackgroundSubtractorMOG2()

        while True:
            success, img = self.get_cap().read()
            # print('justin')
            if success:
                height, width, _ = img.shape
                min_x, min_y = width, height
                max_x = max_y = 0

                blur = cv2.GaussianBlur(img, (5, 5), 10)
                fgmask = fgbg.apply(blur)
                fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

                contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for i in range(len(contours)):
                    if len(contours) > 0:
                        x, y, w, h = cv2.boundingRect(contours[i])

                        # tl = (rect_x, rect_y)
                        # br = (rect_x+rect_w, rect_y+rect_h)

                        min_x, max_x = min(x, min_x), max(x + w, max_x)
                        min_y, max_y = min(y, min_y), max(y + h, max_y)

                        if w > 25 and h > 80:
                            rect = cv2.minAreaRect(contours[i])
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            box = cv2.boxPoints(rect)
                            box_d = np.int0(box)
                            cv2.drawContours(img, [box_d], 0, (0, 255, 0), 3)
                            # cv2.drawContours(blur, contours[i], -1, (255, 0, 0))
                if show:
                    cv2.imshow('Image', blur)
                    cv2.imshow('contour', fgmask)
                print(boxes)
                yield boxes
            yield

    def get_cap(self):
        return self.cap

    def set_cap(self, cam_num):
        self.cap = cam_num


if __name__ == '__main__':
    """
        options {
            arr[]
            arr[]
            tuple(0,0,0)
        }
    """

    v = VisionV3(0)
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
