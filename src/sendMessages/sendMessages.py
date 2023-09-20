#Ao rodar esse script, ir em até 4 segundos para a página do whatsapp web SEM a aba inspecionar aberta
import keyboard
import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))
import time
import random
import pyautogui
from unidecode import unidecode
from src.databaseConfig.firebaseConfig import users_ref

os.environ['PYTHONIOENCODING'] = 'utf-8'

class SendMessages:
    def open_conversation(self):
        time.sleep(4)
        input_search_box_xy = (255, 257) #Talvez o CAIO precise alterar na tela dele
        first_conversation_box_xy = (150, 400) #Talvez o CAIO precise alterar na tela dele
        input_send_message_xy = (880, 952) #Talvez o CAIO precise alterar na tela dele

        users = self.get_users()
        
        for user in users:
            phone_number = unidecode(user.to_dict()["message_sender"]).strip().rstrip(':')
            message_to_be_sent = user.to_dict()["messages"][-1]["text"]

            self.move_to_and_click(xy_position = input_search_box_xy)
            time.sleep(1)
            pyautogui.write(phone_number)
            time.sleep(1)
            self.move_to_and_click(xy_position=first_conversation_box_xy)
            time.sleep(2)
            self.move_to_and_click(xy_position=input_send_message_xy)
            time.sleep(2)
            keyboard.write(message_to_be_sent)
            time.sleep(6)
            pyautogui.hotkey('enter')
            time.sleep(2)
            self.update_user(user.id)

    def move_to_and_click(self, xy_position):
        pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=pyautogui.easeInOutQuad)
        pyautogui.click()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)
    
    def get_users(self):
        users = users_ref.where("need_to_send_answer", "==", True).get()
        return users

    def update_user(self, doc_id):
        users_ref.document(doc_id).update({"need_to_send_answer": False})

SendMessages().open_conversation()
