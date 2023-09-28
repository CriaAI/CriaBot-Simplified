import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
import csv
from src.config import (
    input_search_new_phone_numbers,
    input_send_message_xy, 
    button_start_new_conversation_xy, 
    first_new_conversation_box_xy,
    word_service
)
from src.utils.whatsApp import WhatsApp

class FirstMessage:
    def __init__(self, pyautogui_module, keyboard_module, pyperclip_module, repository, file_path):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.pyperclip = pyperclip_module
        self.repository = repository
        self.file_path = file_path

    def open_conversation(self):
        is_whatsapp_open = WhatsApp(self.pyautogui, self.keyboard, self.pyperclip).is_whatsapp_open()
        if not is_whatsapp_open:
            return

        messages = [
            "Olá, tudo bem?",
            "Aqui é o Caio da CriaAI!",
            "Vocês prestam serviços jurídicos?"
        ]

        with open(self.file_path, 'r') as csv_file:
            phone_numbers_array = csv.reader(csv_file)
            
            for phone_number in phone_numbers_array:
                find_sender_db = self.repository.get_user_by_name(f" {phone_number[0]}: ")
                copied_word = ""

                #If the sender is in the database, he will be ignored
                if len(find_sender_db) > 0:
                    continue
                
                self.move_to_and_click(xy_position=button_start_new_conversation_xy)
                time.sleep(1)
                self.move_to_and_click(xy_position=input_search_new_phone_numbers)
                time.sleep(1)
                self.pyautogui.write(phone_number[0])
                time.sleep(1)
                self.move_to_and_click(xy_position=first_new_conversation_box_xy)
                time.sleep(1)
                self.move_to_and_click(xy_position=input_send_message_xy)
                time.sleep(1)

                for message in messages:
                    self.keyboard.write(message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
                    time.sleep(2)

                self.move_to_and_double_click(xy_position=word_service)
                time.sleep(1)
                copied_word = self.copy_to_variable()
                time.sleep(1)

                if copied_word.strip() == "serviços":
                    self.repository.insert_new_document(f" {phone_number[0]}: ")
                
                self.pyautogui.hotkey('esc')

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def copy_to_variable(self):
        self.pyperclip.copy('')
        self.pyautogui.hotkey('ctrl', 'c')
        return self.pyperclip.paste()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)