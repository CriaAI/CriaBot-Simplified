import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import random
import time
from src.config import screen_variables as sv

class PhoneChip:
    def __init__(self, keyboard_module, pyautogui_module, pyperclip_module):
        self.keyboard = keyboard_module
        self.pyautogui = pyautogui_module
        self.pyperclip = pyperclip_module

    def check_phone_chip(self):
        self.move_to_and_click(sv["profile_picture_xy"])
        time.sleep(1)
        self.move_to_and_click(sv["message_sender_xy"])
        time.sleep(1)
        self.move_to_and_click(sv["message_sender_name_xy"])
        time.sleep(1)
        self.keyboard.press_and_release("ctrl+a")
        time.sleep(0.5)
        message_sender = self.copy_to_variable()
        time.sleep(0.5)
        self.keyboard.press_and_release("esc")
        time.sleep(0.5)
        self.keyboard.press_and_release("esc")
        return message_sender

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def copy_to_variable(self):
        self.pyperclip.copy('')
        self.pyautogui.hotkey('ctrl', 'c')
        return self.pyperclip.paste()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)