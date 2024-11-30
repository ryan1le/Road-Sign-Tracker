from ultralytics import YOLO
import cv2
import cvzone
import math

from classes import MESSAGE_DICT

class detector():
    def __init__(self, parent) -> None:
        self.model = YOLO('../YOLO Weights/yolo11n.pt')
        self.names = self.model.names
        self.object_results = None

        self.object_name = ""
        self.object_class = None
        self.message = ""
        self.conf = None

        self.font = cv2.FONT_HERSHEY_SIMPLEX 

        self.parent = parent

    def do_sign_detection(self, frame):
        results = list(self.model.track(frame, persist=True, classes=39, tracker="bytetrack.yaml"))

        if (len(results[0].boxes)):
            self.object_results = results[0].boxes[0]

            self.object_class = int(self.object_results.cls[0])
            self.object_name = self.names[self.object_class]
            self.message = MESSAGE_DICT[self.object_class]

            x1, y1, x2, y2 = self.object_results.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2-x1, y2-y1

            cvzone.cornerRect(frame, (x1, y1, w, h))

            self.conf = math.ceil((self.object_results.conf[0]*100))

            cv2.putText(frame, self.object_name,  (50, 50),  self.font, 1,  (0, 255, 255),  2,  cv2.LINE_4)
            cv2.putText(frame, self.message,  (50, 700),  self.font, 1,  (0, 255, 255),  2,  cv2.LINE_4)

        else:
            self.object_name = ""
            self.object_class = None
            self.message = ""
            self.conf = None

        self.update_parent_object_detection_state_tracker()

        return frame
    
    def update_parent_object_detection_state_tracker(self):
        self.parent.sign_detected = True if self.object_results != None else False
    
    def get_object_conf(self):
        return self.conf
    
    def get_object_class(self):
        return self.object_class