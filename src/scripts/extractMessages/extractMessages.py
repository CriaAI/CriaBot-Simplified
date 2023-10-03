import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.config import screen_variables as sv
from src.config import user_name
import time
from datetime import datetime
import random
from src.utils.getHtml import GetHtml

class ExtractMessages:
    def __init__(self, pyautogui_module, pyperclip_module, repository, filter_click_type):
        self.pyautogui = pyautogui_module
        self.pyperclip = pyperclip_module
        self.repository = repository
        self.filter_click_type = filter_click_type

    def open_conversation(self):
        if self.filter_click_type == "click":
            self.move_to_and_click(xy_position = sv["filter_box_xy"]) #filter for unread conversations
        else:
            self.move_to_and_double_click(xy_position = sv["filter_box_xy"]) #filter for unread conversations
        time.sleep(1)
        self.move_to_and_click(xy_position=sv["first_conversation_box_xy"])
        time.sleep(2)
        messages = GetHtml(self.pyautogui, self.pyperclip).extract_last_messages()
        current_sender = self.insert_messages(messages)
        return current_sender

    def move_to_and_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)

    def insert_messages(self, messages):
        find_sender_db = []
        
        #finding out who the message sender is
        for message in messages:
            if message["message_sender"].strip().rstrip(':') not in user_name:
                find_sender_db = self.repository.get_user_by_name(message["message_sender"])

                #checking the time of the last message. If it was less than 5 minutes ago, we go to the next message
                last_message = messages[-1]
                message_time = datetime.strptime(last_message["message_date"], "%H:%M, %d/%m/%Y")
                now = datetime.now()

                if (now - message_time).total_seconds() / 60 < 5:
                    return {"sender": last_message["message_sender"].strip().replace(":", "")}
         
                #if the sender is not in the database, he will be added to it
                if len(find_sender_db) == 0:
                    self.repository.insert_new_document(
                        lead=message["message_sender"],
                        message_sender=user_name,
                        messages=[],
                        date=now.strftime("%H:%M, %d/%m/%Y")
                    )

                    find_sender_db = self.repository.get_user_by_phone_number(message["message_sender"])
                    data_to_be_updated = {
                        "stage": 4, 
                        "category": "Lawyer", 
                        "need_to_generate_answer": True
                    }

                    self.repository.update_user_info(find_sender_db[0].id, data_to_be_updated)
                else:
                    self.repository.update_user_info(find_sender_db[0].id, {"need_to_generate_answer": True})
                
                    #if the user stage is 0, after this first interaction, it will be updated to 1
                    stage = find_sender_db[0].to_dict()["stage"]
                    if stage == 0:
                        self.repository.update_user_info(find_sender_db[0].id, {"stage": 1})
                    break
        
        #Now, the messages will be inserted in the db inside the messages array
        doc_id = find_sender_db[0].id
        doc_data = find_sender_db[0].to_dict()

        #Making sure there won't be any repeated messages in the db
        date_time_format = "%H:%M, %d/%m/%Y"
        for message in messages:
            message_to_insert = {
                "sender": message["message_sender"],
                "text": message["message_text"], 
                "date": message["message_date"]
            }
            
            if len(doc_data["messages"]) > 0:
                last_message_date_db = datetime.strptime(doc_data["messages"][-1]["date"], date_time_format)
                last_message_text_db = doc_data["messages"][-1]["text"]
                message_date_time = datetime.strptime(message["message_date"], date_time_format)

                if last_message_date_db > message_date_time or last_message_text_db == message["message_text"]:
                    continue
                else:
                    doc_data["messages"].append(message_to_insert)
            else:
                doc_data["messages"].append(message_to_insert)

        self.repository.update_user_info(doc_id, {"messages": doc_data["messages"]})
        return doc_data["lead"]