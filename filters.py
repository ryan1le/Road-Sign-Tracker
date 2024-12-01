
from collections import deque

class filters():

    def __init__(self, window_size):
        self.window_size = window_size
        self.registered_time = None
        self.window = deque([0] * window_size)

    def update(self, value):
        self.window.popleft()
        self.window.append(value)
    
    def get_activation(self):
        positive = self.window.count(1)
        return float(positive/self.window_size)

    def reg_time(self, time):
        self.registered_time = time

    def is_timeout(self, time, threshold):
        if self.registered_time is not None:
            detection_time = time - self.registered_time
            if detection_time >= threshold:
                return True
            return False
        else:
            return False
    
    def reset(self):
        self.window = deque([0] * self.window_size)
        self.registered_time = None