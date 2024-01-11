import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.config import screen_variables as sv
from src.config import user_name
import time
from datetime import datetime
import random
from src.utils.getHtml import GetHtml
import copy

class ExtractMessages:
    def __init__(self, pyautogui_module, pyperclip_module, bezierMove_module, repository, filter_click_type, last_sender:str):
        self.pyautogui = pyautogui_module
        self.pyperclip = pyperclip_module
        self.bezierMove = bezierMove_module
        self.repository = repository
        self.filter_click_type = filter_click_type
        self.last_sender = last_sender

    def open_conversation(self):
        if self.filter_click_type == "click":
            self.move_to_and_click(xy_position = sv["filter_box_xy"]) #filter for unread conversations
            #self.move_to_and_click(xy_position = sv["filter_box_nao_lidas_xy"]) #only for whatsapp business
            self.scoll_messages_column()
        else:
            self.move_to_and_double_click(xy_position = sv["filter_box_xy"]) #filter for unread conversations
            #self.move_to_and_click(xy_position = sv["filter_box_nao_lidas_xy"]) #only for whatsapp business
        #scroll WhatsApp messages column

        self.move_to_and_click(xy_position=sv["first_conversation_box_xy"])
        time.sleep(2)
        messages = GetHtml(self.pyautogui, self.pyperclip, self.bezierMove).extract_last_messages()
        current_sender = self.insert_messages(messages)
        return current_sender

    def move_to_and_click(self, xy_position):
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.click()

    def move_to(self, xy_position):
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

    def scoll_messages_column(self):
        self.move_to_and_click(xy_position=sv["messages_column_whatsapp"])
        time.sleep(1)
        self.pyautogui.hotkey('end')
        time.sleep(3)

    def move_to_and_double_click(self, xy_position):
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.pyautogui.doubleClick()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)

    def insert_messages(self, messages):
        find_sender_db = []

        #finding out who the message sender is
        for message in messages:
            if user_name not in message["message_sender"].strip().rstrip(':') and message["message_sender"] != " None: ":
                find_sender_db = self.repository.get_user_by_phone_number(message["message_sender"])

                #checking the time of the last message. If it was less than 5 minutes ago, we go to the next message
                #it will be marked as unread later on
                last_message = messages[-1]

                message_time = datetime.strptime(last_message["message_date"], "%H:%M, %d/%m/%Y")
                now = datetime.now()

                if (now - message_time).total_seconds() / 60 < 3: #5:
                    return {"sender": last_message["message_sender"].strip().replace(":", "")}

                #if the sender is not in the database, he will be added to it
                if len(find_sender_db) == 0:
                    self.repository.insert_new_document(
                        lead=message["message_sender"],
                        message_sender=user_name,
                        messages=[],
                        created_at=now.strftime("%H:%M, %d/%m/%Y"),
                        stage=4
                    )

                find_sender_db = self.repository.get_user_by_phone_number(message["message_sender"])
                self.repository.update_user_info(find_sender_db[0].id, {"need_to_generate_answer": True})

                #if the user stage is 0, after this first interaction, it will be updated to 1
                stage = find_sender_db[0].to_dict()["stage"]
                if stage == 0:
                    self.repository.update_user_info(find_sender_db[0].id, {"stage": 1})
                break

        #Now, the messages will be inserted in the db inside the messages array
        doc_id = find_sender_db[0].id
        doc_data = find_sender_db[0].to_dict()
        if doc_data["lead"] == self.last_sender:
            print('repeated sender!!')
            return doc_data["lead"]

        #Making sure there won't be any repeated messages in the db
        date_time_format = "%H:%M, %d/%m/%Y"
        list_of_messages_to_update = copy.deepcopy(doc_data["messages"])

        for message in messages:
            if user_name in message["message_sender"]: #only messages from the lead will be saved in the database
                print('prospect message!')
                continue

            message_to_insert = {
                "sender": message["message_sender"],
                "text": message["message_text"],
                "date": message["message_date"]
            }

            if len(doc_data["messages"]) > 0:
                print(doc_data["messages"][-1]["date"])
                last_message_date_db = datetime.strptime(doc_data["messages"][-1]["date"], date_time_format)
                message_date_time = datetime.strptime(message["message_date"], date_time_format)

                if message_date_time >= last_message_date_db:
                    list_of_messages_to_update.append(message_to_insert)
                else:
                    continue
            else:
                list_of_messages_to_update.append(message_to_insert)

        self.repository.update_user_info(doc_id, {"messages": list_of_messages_to_update})
        return doc_data["lead"]