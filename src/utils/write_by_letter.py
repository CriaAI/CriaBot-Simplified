import keyboard
import time
import json
import random

class WriteByLetter():
    def __init__(self, tipe_base_time:float = 0.1, duration_delta:float = 0.3):
        self.duration_delta = duration_delta
        self.tipe_base_time = tipe_base_time

    def write(self, text:str):
        time_randomization = random.randint(1000*(1-self.duration_delta), 1000*(1+self.duration_delta))/1000
        [keyboard.write(i, delay=self.tipe_base_time*time_randomization) for i in text]
#WriteByLetter().write(text=text)
