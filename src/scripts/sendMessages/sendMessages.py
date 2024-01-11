import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
from unidecode import unidecode
from src.config import video_path
from src.config import screen_variables as sv
from src.utils.phoneChip import PhoneChip
from datetime import datetime
from src.config import message_stage_2, message_stage_3
from src.config import user_name


os.environ['PYTHONIOENCODING'] = 'utf-8'

class SendMessages:
    def __init__(self, pyautogui_module, keyboard_module, pyperclip_module, bezierMove_module, repository):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.pyperclip = pyperclip_module
        self.bezierMove = bezierMove_module
        self.repository = repository

    def open_conversation(self):
        phone_chip = PhoneChip(self.keyboard, self.pyautogui, self.pyperclip)
        #self.message_sender = phone_chip.check_phone_chip()
        self.message_sender = user_name#'Caio'

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
                #self.keyboard.write(last_message)
                self.pasteMessage(text = last_message)
                time.sleep(1)
                self.pyautogui.hotkey('enter')
            elif stage == 2:
                #if the last message in the db is not from the seller, we send the messages below
                if not last_message_sender in f" {self.message_sender}: ":
                    messages = message_stage_2
                    '''["Então, possuo uma empresa que recentemente foi acelerada pela Microsoft e investida pelo maior ecossistema de Legaltechs do país...",
                              "<Vídeo plataforma>",
                              "Dito isso, estamos desenvolvendo uma solução de IA que pode gerar qualquer tipo de documento jurídico do zero e com o embasamento jurídico adequado. Como nossa plataforma ainda está evoluindo, estou buscando advogados interessados em fazer o teste da nossa solução de forma 100% gratuita.",
                              "Se tiver interesse, só mandar um 👍 que eu envio o link!"]'''
                    #self.keyboard.write(messages[0])
                    self.pasteMessage(text = messages[0])
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
                    time.sleep(1)
                    self.send_video()
                    time.sleep(1)
                    self.move_to_and_double_click(sv["video_xy"])
                    time.sleep(2)
                    self.pyautogui.hotkey('enter')
                    time.sleep(1)
                    self.pasteMessage(text = messages[2])
                    #self.keyboard.write(messages[2])
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
                    time.sleep(1)
                    #self.keyboard.write(messages[3])
                    self.pasteMessage(text = messages[3])
                    self.insert_sent_messages(doc_id=user.id, list_of_texts=messages)
                else: #otherwise, we send the message that is in the database
                    #self.keyboard.write(last_message)
                    self.pasteMessage(text = last_message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
            elif stage == 3:
                print('ENTERED STAGE 3!')
                if not last_message_sender in f" {self.message_sender}: ":
                    print('sender different!')
                    messages = message_stage_3
                    '''[
                        #"Segue o link da nossa comunidade de early adopters: https://chat.whatsapp.com/ID6IKjMXhCU1jxPcVz3oix",
                        "Segue o link da plataforma:\nwww.criaai.com",
                        #"Na descrição do grupo AVISOS vai estar o link da plataforma, só acessar o link e criar uma conta gratuita!",
                        #"Vou deixar liberado acesso até hoje para criar sua conta! Só fazer o cadastro e testar à vontade! Não leva nem 1 minuto.",
                        "Vou deixar liberado acesso até hoje para criar sua conta! Só fazer o cadastro e testar à vontade! Não leva nem 1 minuto.",
                        "Para garantir seu acesso, entre na nossa comunidade de early adopters:\nhttps://chat.whatsapp.com/ID6IKjMXhCU1jxPcVz3oix",
                        "E uma dica: Para nosso teste não ser ainda mais um peso na sua semana, indicamos testar a plataforma já buscando economizar o tempo em alguma demanda. Quanto mais real e específico for o caso que você passar para a IA, melhores e mais surpreendentes serão os resultados obtidos 😉"
                    ]'''
                    for message in messages:
                        self.pasteMessage(text = message)
                        #self.keyboard.write(message)
                        time.sleep(1)
                        self.pyautogui.hotkey('enter')
                        time.sleep(1)
                    self.insert_sent_messages(doc_id=user.id, list_of_texts=messages)
                else:
                    self.pasteMessage(text = last_message)
                    #self.keyboard.write(last_message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
            elif stage == 4:
                print(f'Sending custom message to {phone_number}.')
                message_to_be_sent = user.to_dict()["messages"][-1]["text"]
                print(f'Custom message: \n{message_to_be_sent}')
                self.pasteMessage(text = message_to_be_sent)
                #self.keyboard.write(message_to_be_sent)

            time.sleep(4)
            self.pyautogui.hotkey('enter')
            time.sleep(1)

            if stage == 3:
                self.repository.update_user_info(user.id, {"stage": 4, "need_to_send_answer": False})
            else:
                self.repository.update_user_info(user.id, {"need_to_send_answer": False})

    def format_text_to_messages(self, list_of_texts:list[str]):
        return [{
            'text': text,
            'sender': self.message_sender,
            'date': datetime.now().strftime("%H:%M, %d/%m/%Y")
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
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def copy_to_variable(self):
        self.pyperclip.copy("")
        self.pyautogui.hotkey("ctrl", "c")
        return self.pyperclip.paste()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)

    def pasteMessage(self, text:str):
        self.pyperclip.copy(text)
        time.sleep(0.2)
        self.pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
