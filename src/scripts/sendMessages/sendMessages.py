#Ao rodar esse script, ir em até 4 segundos para a página do whatsapp web SEM a aba inspecionar aberta
import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
from unidecode import unidecode
from src.config import video_path
from src.config import screen_variables as sv

os.environ['PYTHONIOENCODING'] = 'utf-8'

class SendMessages:
    def __init__(self, pyautogui_module, keyboard_module, pyperclip_module, repository):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.pyperclip = pyperclip_module
        self.repository = repository

    def open_conversation(self):
        users = self.repository.get_users_by_need_to_send_answer()

        for user in users:
            phone_number = unidecode(user.to_dict()["message_sender"]).strip().rstrip(':')
            stage = user.to_dict()["stage"]

            self.move_to_and_click(xy_position = sv["input_search_box_xy"])
            time.sleep(1)
            self.pyautogui.write(phone_number)
            time.sleep(1)
            self.move_to_and_click(xy_position=sv["first_conversation_box_xy"])
            time.sleep(2)
            self.move_to_and_click(xy_position=sv["input_send_message_xy"])
            time.sleep(2)

            if stage == 0 or stage == 1:
                continue
            elif stage == 2:
                self.keyboard.write("Minha empresa desenvolveu recentemente uma Inteligência Artificial específica para advogados!")
                time.sleep(1)
                self.pyautogui.hotkey('enter')
                time.sleep(1)
                self.send_video()
                time.sleep(1)
                self.move_to_and_double_click(sv["video_xy"])
                time.sleep(2)
                self.pyautogui.hotkey('enter')
                time.sleep(1)
                self.keyboard.write(
                    """Estou buscando advogados interessados em fazer o teste da nossa solução de forma 100% gratuita. 
                    Se tiver interesse, só mandar um 👍 que eu envio o link!"""
                )
            elif stage == 3:
                messages = [
                    "Segue o link: https://criaai.com/",
                    """Vou deixar liberado acesso até hoje para criar sua conta! Só fazer o cadastro e testar à vontade! 
                    Não leva nem 1 minuto.""",
                    """E uma dica: Para nosso teste não ser ainda mais um peso na sua semana, indicamos testar a plataforma já 
                    buscando economizar o tempo em alguma demanda. Quanto mais real e específico for o caso que você passar para a 
                    IA, melhores e mais surpreendentes serão os resultados obtidos 😉"""
                ]

                for message in messages:
                    self.keyboard.write(message)
                    time.sleep(1)
                    self.pyautogui.hotkey('enter')
                    time.sleep(1)
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

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)
