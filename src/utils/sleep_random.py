import time
import random

class SleepRandom():
    def __init__(self, duration_delta:float = 0.3):
        self.duration_delta = duration_delta
    def sleep(self, duration):
        time_randomization = random.randint(1000*(1-self.duration_delta), 1000*(1+self.duration_delta))/1000
        time.sleep(time_randomization*duration)