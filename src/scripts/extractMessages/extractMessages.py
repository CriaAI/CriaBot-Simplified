#extractMessages.py
# Quando rodar o projeto, ir para a interface do whatsapp em até 4 segundos
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from bs4 import BeautifulSoup
import time
from datetime import datetime
import random
from src.errors.extractMessagesErrors import MissingHtmlError

class ExtractMessages:
    def __init__(self, pyautogui_module, repository, get_html_from_whatsapp, filter_click_type):
        self.pyautogui = pyautogui_module
        self.repository = repository
        self.get_html_from_whatsapp = get_html_from_whatsapp
        self.filter_click_type = filter_click_type

    def open_conversation(self):
        filter_box_xy = (465, 241) #Talvez o CAIO precise alterar na tela dele
        first_conversation_box_xy = (150, 400) #Talvez o CAIO precise alterar na tela dele
        if self.filter_click_type == "click":
            self.move_to_and_click(xy_position = filter_box_xy) #filter for unread conversations
        else:
            self.move_to_and_double_click(xy_position = filter_box_xy) #filter for unread conversations
        time.sleep(1)
        self.move_to_and_click(xy_position=first_conversation_box_xy)
        time.sleep(2)
        current_sender = self.extract_last_messages()
        return current_sender

    def extract_last_messages(self):
        try:
            html = self.get_html_from_whatsapp.extract_HTML()
            soup = BeautifulSoup(html, 'html.parser')
            my_divs = soup.find_all("div", {"class": "_21Ahp"})
            
            if len(my_divs) == 0:
                raise MissingHtmlError("There are no html components for this conversation.")

            messages_list = []

            for element in my_divs:
                message_meta_data:str = element.parent.get('data-pre-plain-text') #Sometimes it returns None

                if message_meta_data == None:
                    continue

                message_date = message_meta_data.split(']')[0].split('[')[-1]
                message_sender = "]".join(message_meta_data.split(']')[1:])
                message_text:str = element.find("span", {"class": "_11JPr selectable-text copyable-text"}) #Sometimes it returns None
                
                if message_text == None:
                    message = {
                        'message_text': 'Não foi possível extrair essa mensagem', 
                        'message_sender': message_sender,
                        'message_date': message_date
                    }
                    messages_list.append(message)
                    continue
                
                message_text = message_text.text
                message = {'message_text': message_text, 'message_sender': message_sender, 'message_date': message_date}
                messages_list.append(message)
            current_sender = self.insert_messages(messages_list)
            return current_sender
        except MissingHtmlError as err:
            return err

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)

    def insert_messages(self, messages):
        #we need to find who the sender is to create the document in the db (cannot be the seller)
        find_sender_db = []

        for message in messages:
            if message["message_sender"] != " Fran Hahn: ": #CAIO terá que colocar como está o nome dele
                find_sender_db = self.repository.get_user_by_name(message["message_sender"])
                
                #If the sender is not in the database yet, a new document will be created for them
                if len(find_sender_db) == 0:
                    self.repository.insert_new_document(message["message_sender"])
                    find_sender_db = self.repository.get_user_by_name(message["message_sender"]) #need to do that to find out the id that was created in the db
                else:
                    self.repository.update_need_to_generate_answer(find_sender_db[0].id, {"need_to_generate_answer": True})
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
                        "date": message["message_date"]
                    })
            else:
                doc_data["messages"].append({
                    "sender": message["message_sender"],
                    "text": message["message_text"], 
                    "date": message["message_date"]
                })

        self.repository.update_messages_array(doc_id, doc_data["messages"])
        return doc_data["message_sender"]