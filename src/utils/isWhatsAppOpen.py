import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.config import path_to_img_dark_theme, path_to_img_light_theme

class IsWhatsAppOpen:
    def __init__(self, pyautogui):
        self.pyautogui = pyautogui

    def locate_img_on_screen(self):
        image1 = self.pyautogui.locateOnScreen(path_to_img_light_theme)
        image2 = self.pyautogui.locateOnScreen(path_to_img_dark_theme)
    
        if image1 is None and image2 is None:
            return False
        
        return True