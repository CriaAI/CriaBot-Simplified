import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
from src.config import (
    input_search_box_xy, 
    return_button_inside_input_with_inspect_tool_xy, 
    return_button_inside_input_without_inspect_tool_xy
)

class WhatsApp:
    def __init__(self, pyautogui_module, keyboard_module, pyperclip_module):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.pyperclip = pyperclip_module

    def is_whatsapp_open(self):
        time.sleep(4)
        self.move_to_and_click(input_search_box_xy)
        time.sleep(1)
        self.keyboard.write("checando")
        time.sleep(1)
        self.move_to_and_double_click(input_search_box_xy)
        time.sleep(1)
        word_copied = self.copy_to_variable()
        time.sleep(1)
        if word_copied == "checando":
            self.move_to_and_click(return_button_inside_input_without_inspect_tool_xy)
            time.sleep(1)
            self.move_to_and_click(return_button_inside_input_with_inspect_tool_xy)
            return True
        else:
            return False

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def copy_to_variable(self):
        self.pyautogui.hotkey('ctrl', 'c')
        return self.pyperclip.paste()
    
    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)