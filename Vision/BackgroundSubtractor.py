import cv2


class VisionV3:

    def __init__(self, cam_number):
        self.cap = cv2.VideoCapture(cam_number)

        self.width = 640
        self.height = 480

        self.cap.set(cv2.CAP_PROP_FPS, 15.0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.min_x, self.min_y = self.width, self.height
        self.max_x, self.max_y = 0, 0

        self.tl = (0, 0)
        self.br = (0, 0)

        self.box_ori = None
        self.prev_box = None

    def vision_generator(self, show=False, non_max_suppression=True):

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
                self.min_x, self.min_y = width, height
                self.max_x, self.max_y = 0, 0

                for i in range(len(contours)):
                    x, y, w, h = cv2.boundingRect(contours[i])

                    if w > 25 and h > 80:
                        if non_max_suppression:
                            self.tl, self.br = self.non_max_suppression(x, y, w, h)
                        else:
                            self.tl = (x, y)
                            self.br = (x + w, y + h)

                        self.check_boxes()

                if show:
                    cv2.rectangle(img, self.tl, self.br, (255, 0, 0), 2)
                    print(self.box_ori)

                    cv2.imshow('Image', img)
                    cv2.imshow('contour', fgmask)

                yield self.box_ori
            yield

    def check_boxes(self):
        self.prev_box = self.box_ori
        self.box_ori = (self.tl, self.br)

        count = 0
        if self.prev_box == self.box_ori:
            count += 1

            if count > 15:
                self.box_ori = None
                self.prev_box = None

    def get_cap(self):
        return self.cap

    def set_cap(self, cam_num):
        self.cap = cam_num

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_min(self, x, y):
        self.min_x = x
        self.min_y = y

    def set_max(self, x, y):
        self.max_x = x
        self.max_y = y

    def non_max_suppression(self, x_coord, y_coord, w, h):
        self.min_x, self.max_x = min(x_coord, self.min_x), max(x_coord + w, self.max_x)
        self.min_y, self.max_y = min(y_coord, self.min_y), max(y_coord + h, self.max_y)

        self.tl = (self.min_x, self.min_y)
        self.br = (self.max_x, self.max_y)

        return self.tl, self.br


if __name__ == '__main__':
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
