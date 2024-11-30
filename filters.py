
from collections import deque

class filters():

    def __init__(self, window_size):
        self.window_size = window_size
        self.window = deque([0] * window_size)

    def update(self, value):
        self.window.popleft()
        self.window.append(value)
    
    def get_activation(self):
        positive = self.window.count(1)
        return float(positive/self.window_size)
    
    def reset(self):
        self.window = deque([0] * self.window_size)