import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
from unidecode import unidecode
from src.config import video_path
from src.config import screen_variables as sv
from src.utils.phoneChip import PhoneChip
from datetime import datetime

os.environ['PYTHONIOENCODING'] = 'utf-8'

class SendMessages:
    def __init__(self, pyautogui_module, keyboard_module, pyperclip_module, repository):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.pyperclip = pyperclip_module
        self.repository = repository

    def open_conversation(self):
        phone_chip = PhoneChip(self.keyboard, self.pyautogui, self.pyperclip)
        self.message_sender = phone_chip.check_phone_chip()

        users = self.repository.get_users_by_need_to_send_answer(self.message_sender)

        for user in users:
            phone_number = unidecode(user.to_dict()["lead"]).strip().rstrip(":")
            stage = user.to_dict()["stage"]
            self.last_messages = user.to_dict()["messages"]
            last_message = self.last_messages[-1]["text"]
            last_message_sender = self.last_messages[-1]["sender"]

            self.move_to_and_click(xy_position = sv["input_search_box_xy"])
            time.sleep(1)
            self.pyautogui.write(phone_number)
            time.sleep(1)
            self.move_to_and_click(xy_position=sv["first_conversation_box_xy"])
            time.sleep(2)
            self.move_to_and_click(xy_position=sv["input_send_message_xy"])
            time.sleep(2)

            if stage == 1: #in this case, the lead will receive a personalized answer
                self.keyboard.write(last_message)
                time.sleep(1)
                self.pyautogui.hotkey('enter')
            elif stage == 2:
                #if the last message in the db is not from the seller, we send the messages below
                if last_message_sender != f" {self.message_sender}: ":
                    messages = ["Minha empresa desenvolveu recentemente uma Inteligência Artificial específica para advogados!",
                              "<Vídeo plataforma>",
                              "Estou buscando advogados interessados em fazer o teste da nossa solução de forma 100% gratuita.\nSe tiver interesse, só mandar um 👍 que eu envio o link!"]
                    self.keyboard.write(messages[0])
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
                    time.sleep(1)
                    self.send_video()
                    time.sleep(1)
                    self.move_to_and_double_click(sv["video_xy"])
                    time.sleep(2)
                    self.pyautogui.hotkey('enter')
                    time.sleep(1)
                    self.keyboard.write(messages[2])
                    self.insert_sent_messages(doc_id=user.id, list_of_texts=messages)
                else: #otherwise, we send the message that is in the database
                    self.keyboard.write(last_message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
            elif stage == 3:
                if last_message_sender != f" {self.message_sender}: ":
                    messages = [
                        "Segue o link: https://criaai.com/",
                        "Vou deixar liberado acesso até hoje para criar sua conta! Só fazer o cadastro e testar à vontade! Não leva nem 1 minuto.",
                        "E uma dica: Para nosso teste não ser ainda mais um peso na sua semana, indicamos testar a plataforma já buscando economizar o tempo em alguma demanda. Quanto mais real e específico for o caso que você passar para a IA, melhores e mais surpreendentes serão os resultados obtidos 😉"
                    ]

                    for message in messages:
                        self.keyboard.write(message)
                        time.sleep(1)
                        self.pyautogui.hotkey('enter')
                        time.sleep(1)
                    self.insert_sent_messages(doc_id=user.id, list_of_texts=messages)
                else:
                    self.keyboard.write(last_message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
            elif stage == 4:
                message_to_be_sent = user.to_dict()["messages"][-1]["text"]
                self.keyboard.write(message_to_be_sent)

            time.sleep(4)
            self.pyautogui.hotkey('enter')
            time.sleep(1)

            if stage == 3:
                self.repository.update_user_info(user.id, {"stage": 4, "need_to_send_answer": False})
            else:
                self.repository.update_user_info(user.id, {"need_to_send_answer": False})

    def format_text_to_messages(self, list_of_texts:list[str]):
        return [{
            'message_text': text,
            'message_sender': self.message_sender,
            'message_date': datetime.now().strftime("%H:%M, %d/%m/%Y")
        } for text in list_of_texts]


    def insert_sent_messages(self, doc_id:str, list_of_texts:list):
        list_of_messages_to_update = self.format_text_to_messages(list_of_texts)
        self.repository.update_user_info(doc_id, {"messages": self.last_messages + list_of_messages_to_update})

    def send_video(self):
        self.move_to_and_click(sv["attach_file_xy"])
        time.sleep(1)
        self.move_to_and_click(sv["photos_and_videos_xy"])
        time.sleep(1)
        self.move_to_and_click(sv["path_to_video_xy"])
        time.sleep(2)
        self.keyboard.write(video_path)
        time.sleep(1)
        self.pyautogui.hotkey('enter')

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def copy_to_variable(self):
        self.pyperclip.copy("")
        self.pyautogui.hotkey("ctrl", "c")
        return self.pyperclip.paste()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)
