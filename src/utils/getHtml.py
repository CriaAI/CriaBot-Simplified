import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
import random
from bs4 import BeautifulSoup

class GetHtml:
    def __init__(self, pyautogui_module, pyperclip_module):
        self.pyautogui = pyautogui_module
        self.pyperclip = pyperclip_module

    def extract_HTML(self):
        htmlXY = (1800, 205)
        self.move_to_and_click(xy_position=htmlXY)
        return self.copy_to_variable()

    def extract_last_messages(self):
        html = self.extract_HTML()
        soup = BeautifulSoup(html, 'html.parser')
        my_divs = soup.find_all("div", {"class": ["_21Ahp", "_1kgzQ"]})

        messages_list = []

        for element in my_divs:
            message_meta_data:str = element.parent.get('data-pre-plain-text') #Sometimes it returns None

            if message_meta_data == None:
                user = soup.find("span", class_="l7jjieqr")
                print("Not possible to extract this message")

                if len(messages_list) > 0:
                    date = messages_list[-1]["message_date"]
                else:
                    date = ""

                message = {
                    "message_text": 'Não foi possível extrair essa mensagem',
                    "message_sender": f" {user.get('title')}: ",
                    "message_date": date
                }

                messages_list.append(message)
                continue

            message_date = message_meta_data.split(']')[0].split('[')[-1]
            message_sender = "]".join(message_meta_data.split(']')[1:])
            #text
            message_text:str = element.find("span", {"class": "_11JPr selectable-text copyable-text"}) #Sometimes it returns None
            if message_text != None:
                message_text = message_text.text
                message = {'message_text': message_text, 'message_sender': message_sender, 'message_date': message_date}
                messages_list.append(message)
                continue
            #emoji
            emoji_text:str = element.find("span", {"class": "Ov-s3"}).find("img")
            if emoji_text != None:
                emoji_text = emoji_text.get('data-plain-text')
                message = {'message_text': emoji_text, 'message_sender': message_sender, 'message_date': message_date}
                messages_list.append(message)
                continue
            if message_text == None:
                print("Not possible to extract this message")
                message = {
                    'message_text': 'Não foi possível extrair essa mensagem',
                    'message_sender': message_sender,
                    'message_date': message_date
                }
                messages_list.append(message)
                continue

        #if any dates are empty, the date will be replaced by the next message date that is not empty
        i = 0
        for message in messages_list:
            if message["message_date"] == "":
                for j in range(i, len(messages_list)):
                    if messages_list[j+1]["message_date"] != "":
                        message["message_date"] = messages_list[j+1]["message_date"]
                        break
            i += 1

        return messages_list

    def get_html_from_start_page(self):
        time.sleep(4)
        html = self.extract_HTML()

        if html == "":
            return

        soup = BeautifulSoup(html, 'html.parser')
        title_html = soup.find('title')
        title_text = title_html.get_text()
        return title_text

    def copy_to_variable(self):
        self.pyperclip.copy('')
        self.pyautogui.hotkey('ctrl', 'c')
        return self.pyperclip.paste()

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.click()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)