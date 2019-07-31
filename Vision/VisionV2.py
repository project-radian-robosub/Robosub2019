import cv2


class VisionV2:

    def __init__(self, cam_number):
        self.cap = cv2.VideoCapture(cam_number)

        self.cap.set(cv2.CAP_PROP_FPS, 15.0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def vision_generator(self, options, show=False):
        option = options
        boxes = {}

        while self.get_cap().isOpened():
            success, img = self.get_cap()

            if success:
                img = cv2.GaussianBlur(img, (5, 5), 10)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                low_hsv = option['mask_low']
                high_hsv = option['mask_high']

                mask = (img, low_hsv, high_hsv)
                mask = cv2.blur(mask, (3, 3))

                ret, thresh = cv2.threshold(mask, option['threshold'])

                img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for i in len(contours):
                    if len(contours > 0):
                        rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(contours[i])

                        tl = tuple(rect_x, rect_y)
                        br = tuple(rect_x+rect_w, rect_y+rect_h)

                        boxes[i].append({tl, br})

                if show:
                    cv2.rectangle = (img, rect_x, rect_y, (rect_x+rect_w), (rect_y+rect_h), (0, 255, 0), 1)
                    cv2.imshow('Image', img)

                    cv2.imshow('Mask', mask)

                    cv2.imshow('Threshold', thresh)

                    img2 = cv2.drawContours(img2, contours, -1, (0, 255, 0))
                    cv2.imshow('Contours', img2)
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
        'mask_low': [0, 85, 150],
        'mask_high': [15, 250, 255],
        'threshold': tuple('0, 0, 0')
    }

    v = VisionV2(0)

    while True:
        v.vision_generator(orange_options, True)

