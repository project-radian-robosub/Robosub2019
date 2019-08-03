import datetime
import cv2
from PressureSensor import Pressure
import IMU


class Telemetry:

    def __init__(self, front_cam, down_cam):
        self.p = Pressure()

        self.date_time = datetime.today()
        self.path = 'home/stewe951/Documents/Telemetry/'

        self.imu_doc = open('%s_IMU_Telemetry' % self.date_time, 'w+')
        self.front_cap = cv2.VideoCapture(front_cam)
        self.down_cap = cv2.VideoCapture(down_cam)

    def write_telemetry_gen(self):
        front_vid = cv2.VideoWriter((self.get_path()+'%s_Front_Cam.avi'%self.date_time),
                                    cv2.VideoWriter_fourcc(*'XVID'),
                                    15.0, (416, 416), True)

        down_vid = cv2.VideoWriter((self.get_path()+'%_Down_Cam.avi'%self.date_time),
                                   cv2.VideoWriter_fourcc(*'XVID'),
                                   15.0, (416, 416), True)
        while True:
            front_ret, front_image = self.get_cap('Front')
            down_ret, down_image = self.get_cap('Down')

            if front_ret:
                front_vid.write(front_image)

            if down_ret:
                down_vid.write(down_image)

            imu_data = [self.get_pressure_sensor().get_val(), list(IMU.sensor.magnetic), list(IMU.sensor.euler)]
            self.imu_doc.write(str(imu_data))

            yield

    def get_cap(self, cam):
        if cam == 'Front':
            return self.front_cap
        elif cam == 'Down':
            return self.down_cap
        else:
            print('There has been an error in get_cap')
            return

    def get_path(self):
        return self.path

    def get_pressure_sensor(self):
        return self.p

    def close_telemetry(self):
        self.get_cap('Front').release()
        self.get_cap('Front').release()

        cv2.destroyAllWindows()
        cv2.destroyAllWindows()
        cv2.destroyAllWindows()

    '''
    @staticmethod
    def _set_cv_cap(cam):
        cam.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 416)
        cam.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, 416)
    '''


if __name__ == '__main__':
    t = Telemetry()

    while True:
        t.write_telemetry_gen()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    t.close_telemetry()
