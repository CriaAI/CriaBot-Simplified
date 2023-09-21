import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import random

class GetHtmlFromWhatsApp:
    def __init__(self, pyautogui_module, pyperclip_module):
        self.pyautogui = pyautogui_module
        self.pyperclip = pyperclip_module
        
    def extract_HTML(self):
        htmlXY = (1800, 205)
        self.move_to_and_click(xy_position=htmlXY)
        return self.copy_to_variable()
    
    def copy_to_variable(self):
        self.pyautogui.hotkey('ctrl', 'c')
        return self.pyperclip.paste()

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.click()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)