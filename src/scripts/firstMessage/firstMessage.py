import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
import csv
from src.config import (
    input_search_new_phone_numbers,
    input_send_message_xy, 
    button_start_new_conversation_xy, 
    return_button_xy,
    first_new_conversation_box_xy,
    path_to_img_dark_theme,
    path_to_img_light_theme
)

class FirstMessage:
    def __init__(self, pyautogui_module, keyboard_module, repository, file_path):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.repository = repository
        self.file_path = file_path

    def open_conversation(self):
        time.sleep(4)

        messages = [
            "Olá, tudo bem?",
            "Aqui é o Caio da CriaAI!",
            "Vocês prestam serviços jurídicos?"
        ]

        with open(self.file_path, 'r') as csv_file:
            phone_numbers_array = csv.reader(csv_file)
            
            for phone_number in phone_numbers_array:
                self.move_to_and_click(xy_position = button_start_new_conversation_xy)
                time.sleep(1)
                self.move_to_and_click(xy_position = input_search_new_phone_numbers)
                time.sleep(1)
                self.pyautogui.write(phone_number[0])
                time.sleep(1)
                self.move_to_and_click(xy_position=first_new_conversation_box_xy)
                time.sleep(1)

                image1 = self.pyautogui.locateOnScreen(path_to_img_light_theme)
                image2 = self.pyautogui.locateOnScreen(path_to_img_dark_theme)
                
                if image1 is None and image2 is None:
                    self.move_to_and_click(xy_position = return_button_xy)
                    continue

                find_sender_db = self.repository.get_user_by_name(phone_number[0])
                
                #If the sender is not in the database yet, a new document will be created for them
                if len(find_sender_db) == 0:
                    self.repository.insert_new_document(f" {phone_number[0]}: ")
                else:
                    continue

                self.move_to_and_click(xy_position=input_send_message_xy)
                time.sleep(1)

                for message in messages:
                    self.keyboard.write(message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
                    time.sleep(2)

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)