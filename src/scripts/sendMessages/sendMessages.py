#Ao rodar esse script, ir em até 4 segundos para a página do whatsapp web SEM a aba inspecionar aberta
import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
from unidecode import unidecode

os.environ['PYTHONIOENCODING'] = 'utf-8'

class SendMessages:
    def __init__(self, pyautogui_module, keyboard_module, repository):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.repository = repository

    def open_conversation(self):
        time.sleep(4)
        input_search_box_xy = (255, 257) #Talvez o CAIO precise alterar na tela dele
        first_conversation_box_xy = (150, 400) #Talvez o CAIO precise alterar na tela dele
        input_send_message_xy = (880, 952) #Talvez o CAIO precise alterar na tela dele

        users = self.repository.get_users_by_need_to_send_answer()
        
        for user in users:
            phone_number = unidecode(user.to_dict()["message_sender"]).strip().rstrip(':')
            message_to_be_sent = user.to_dict()["messages"][-1]["text"]

            self.move_to_and_click(xy_position = input_search_box_xy)
            time.sleep(1)
            self.pyautogui.write(phone_number)
            time.sleep(1)
            self.move_to_and_click(xy_position=first_conversation_box_xy)
            time.sleep(2)
            self.move_to_and_click(xy_position=input_send_message_xy)
            time.sleep(2)
            self.keyboard.write(message_to_be_sent)
            time.sleep(6)
            self.pyautogui.hotkey('enter')
            time.sleep(2)
            self.repository.update_need_to_send_answer(user.id, {"need_to_send_answer": False})

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)
