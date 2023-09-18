#extractMessages.py
# Quando rodar o projeto, ir para a interface do whatsapp em até 4 segundos
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import time
from datetime import datetime
import random
import pyautogui
import pyperclip
from bs4 import BeautifulSoup
from src.databaseConfig.firebaseConfig import users_ref

SECS_BETWEEN_KEYS = 0.2
filter_click_type = "click"

class ExtractMessages:
    def open_conversation(self):
        filter_box_xy = (465, 241) #Talvez o CAIO precise alterar na tela dele
        first_conversation_box_xy = (150, 400) #Talvez o CAIO precise alterar na tela dele
        if filter_click_type == "click":
            self.move_to_and_click(xy_position = filter_box_xy) #filter for unread conversations
        else:
            self.move_to_and_double_click(xy_position = filter_box_xy) #filter for unread conversations
        time.sleep(1)
        self.move_to_and_click(xy_position=first_conversation_box_xy)
        time.sleep(2)
        current_sender = self.extract_last_messages()
        return current_sender

    def extract_last_messages(self):
        html = self.extract_HTML()
        soup = BeautifulSoup(html, 'html.parser')
        my_divs = soup.find_all("div", {"class": "_21Ahp"})
        messages_list = []

        for element in my_divs:
            message_meta_data:str = element.parent.get('data-pre-plain-text') #Sometimes it returns None

            if message_meta_data == None:
                continue

            message_date = message_meta_data.split(']')[0].split('[')[-1]
            message_sender = "]".join(message_meta_data.split(']')[1:])
            message_text:str = element.find("span", {"class": "_11JPr selectable-text copyable-text"}) #Sometimes it returns None
            
            if message_text == None:
                continue
            
            message_text = message_text.text
            message = {'message_text': message_text, 'message_sender': message_sender, 'message_date': message_date}
            messages_list.append(message)
        current_sender = self.insert_messages_database(messages_list)
        return current_sender

    def extract_HTML(self):
        htmlXY = (1800, 205)
        self.move_to_and_click(xy_position=htmlXY)
        return self.copy_to_variable()

    def copy_to_variable(self):
        pyautogui.hotkey('ctrl', 'c')
        return pyperclip.paste()

    def move_to_and_click(self, xy_position):
        pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        pyautogui.doubleClick()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)
    
    def get_user_database(self, message):
        sender_to_search = message["message_sender"]
        find_sender_db = users_ref.where("message_sender", "==", sender_to_search).get()
        return find_sender_db
    
    def update_user_database(self, doc_id, messages):
        users_ref.document(doc_id).update({"messages": messages})

    def insert_messages_database(self, messages):
        #we need to find who the sender is to create the document in the db (cannot be the seller)
        find_sender_db = []
        for message in messages:
            if message["message_sender"] != " Fran Hahn: ": #CAIO terá que colocar como está o nome dele
                find_sender_db = self.get_user_database(message)
                
                #If the sender is not in the database yet, a new document will be created for them
                if len(find_sender_db) == 0:
                    users_ref.add({
                        "message_sender": message["message_sender"],
                        "messages_to_be_answered": True,
                        "messages": []
                    })
                    find_sender_db = self.get_user_database(message) #need to do that to find out the id that was created in the db
                break
        
        #Now, the messages will be inserted in the db inside the messages array
        doc_id = find_sender_db[0].id
        doc_data = find_sender_db[0].to_dict()

        #Making sure that there won't be repeated messages in the db
        date_time_format = "%H:%M, %d/%m/%Y"
        for message in messages:
            if len(doc_data["messages"]) > 0:
                last_message_date_db = datetime.strptime(doc_data["messages"][-1]["date"], date_time_format)
                last_message_text_db = doc_data["messages"][-1]["text"]
                message_date_time = datetime.strptime(message["message_date"], date_time_format)
                
                if last_message_date_db > message_date_time or last_message_text_db == message["message_text"]:
                    continue
                else:
                    doc_data["messages"].append({
                        "sender": message["message_sender"],
                        "text": message["message_text"], 
                        "date": message["message_date"],
                        "was_answered": False
                    })
            else:
                doc_data["messages"].append({
                    "sender": message["message_sender"],
                    "text": message["message_text"], 
                    "date": message["message_date"],
                    "was_answered": False
                })

        self.update_user_database(doc_id, doc_data["messages"])
        return doc_data["message_sender"]

previous_sender = ""
while True:
    time.sleep(4)
    current_sender = ExtractMessages().open_conversation()

    if filter_click_type == "click":
        filter_click_type = "double_click"

    #This is to avoid an infinite loop
    if previous_sender == current_sender:
        break

    previous_sender = current_sender