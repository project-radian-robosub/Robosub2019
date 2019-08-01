import cv2
import numpy as np


class VisionV2:

    def __init__(self, cam_number):
        self.cap = cv2.VideoCapture(cam_number)

        self.cap.set(cv2.CAP_PROP_FPS, 15.0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def vision_generator(self, options, show=False):
        option = options
        boxes = ['null']

        print(option)
        while True:
            success, img = self.get_cap().read()
            # print('justin')
            if success:
                print('hi')
                img = cv2.GaussianBlur(img, (5, 5), 10)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                low_hsv = option['mask_low']
                high_hsv = option['mask_high']

                mask = cv2.inRange(img, np.array(low_hsv), np.array(high_hsv))
                mask = cv2.GaussianBlur(mask, (3, 3), 5)
                t = option['threshold']
                ret, thresh = cv2.threshold(mask, t[0], t[1], t[2])

                img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for i in range(len(contours)):
                    if len(contours) > 0:
                        rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(contours[i])

                        tl = (rect_x ,rect_y)
                        br = (rect_x+rect_w, rect_y+rect_h)

                        if (rect_h*rect_w) >100:
                            boxes.append({'tl': tl})
                            boxes.append({'br': br})
                            del boxes[0]

                    if show:
                        cv2.rectangle = (img, rect_x, rect_y, (rect_x+rect_w), (rect_y+rect_h), (0, 255, 0), 1)

                        # cv2.imshow('Mask', mask)

                        # cv2.imshow('Threshold', thresh)

                    # img2 = cv2.drawContours(img2, contours, -1, (0, 255, 0))

                if show:
                    cv2.imshow('Image', img2)
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

    orange_options = {
        'mask_low': [0, 0, 94],
        'mask_high': [68, 83, 192],
        'threshold': [127, 255, 0]
    }

    v = VisionV2(0)
    print('Starting Loop')
    x = v.vision_generator(orange_options, True)

    while True:
        x.__next__()
        # print('running')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    v.get_cap().release()
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()

