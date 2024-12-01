from ultralytics import YOLO
import cv2
import cvzone
import math

from classes import MESSAGE_DICT
from state_machine import *
from filters import *
from detector import *

from settings import *

class SignDetectionSystem():
    def __init__(self):
        self.system_state = STATE['idle']
        self.sign_detected = False

        self.stream = cv2.VideoCapture(0)
        self.stream.set(3, 1280)
        self.stream.set(4, 720)

        self.idle_confirm_filter = filters(IDLE_CONFIRM_FILTER_SIZE)
        self.confirm_detected_filter = filters(CONFIRM_DETECTED_FILTER_SIZE)
        self.reset_filter = filters(RESET_FILTER_SIZE)

        self.idle_confirm_trigger = 0.0
        self.confirm_detected_trigger = 0.0

        self.detector = detector(self)

    def main(self):
        while True:
            success, img = self.stream.read()
            
            frame = self.detector.do_sign_detection(img)

            self.idle_confirm_filter.update(self.sign_detected)
            self.confirm_detected_filter.update(self.sign_detected)

            self.idle_confirm_trigger = self.idle_confirm_filter.get_activation()
            self.confirm_detected_trigger = self.confirm_detected_filter.get_activation()

            cv2.imshow("Image", frame)
            key = cv2.waitKey(1)
            
            if key == 27:  # Press ESC to exit
                self.stream.release()
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    system = SignDetectionSystem()
    system.main()