import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.config import screen_variables as sv
from src.config import user_name
from src.utils.phoneChip import PhoneChip
import time
from datetime import datetime
import random
import csv
from src.config import message_stage_1


class FirstMessage:
    def __init__(self, pyautogui_module, keyboard_module, pyperclip_module, get_html, repository, file_path, bezierMove, writeByLetter, sleepRandom):
        self.pyautogui = pyautogui_module
        self.keyboard = keyboard_module
        self.pyperclip = pyperclip_module
        self.get_html = get_html
        self.repository = repository
        self.file_path = file_path
        self.bezierMove = bezierMove
        self.writeByLetter = writeByLetter
        self.sleepRandom = sleepRandom
    def open_conversation(self):
        #phone_chip = PhoneChip(self.keyboard, self.pyautogui, self.pyperclip)
        message_sender = user_name#'Caio'
        #phone_chip.check_phone_chip()
        print(message_sender)

        messages = message_stage_1

        with open(self.file_path, 'r') as csv_file:
            phone_numbers_array = csv.reader(csv_file)
            line = 1

            #we will only send 10 messages at a time
            for phone_number in phone_numbers_array:
                if line > 10:
                    break

                self.move_to_and_click(xy_position=sv["button_start_new_conversation_xy"])
                #time.sleep(1)
                self.sleepRandom.sleep(1)
                self.move_to_and_click(xy_position=sv["input_search_new_phone_numbers"])
                #time.sleep(1)
                self.sleepRandom.sleep(1)
                self.pyautogui.hotkey('ctrl', 'a')
                #self.pyautogui.write(phone_number[0])
                self.writeByLetter.write(phone_number[0])
                #time.sleep(1)
                self.sleepRandom.sleep(1)
                self.move_to_and_click(xy_position=sv["first_new_conversation_box_xy"])
                #time.sleep(0.5)
                self.sleepRandom.sleep(0.5)

                #Get wpp user name
                wpp_user_name = self.get_html.extract_user()
                print(f" wpp_user_name: {wpp_user_name}")
                if not wpp_user_name:
                    continue
                find_sender_db = self.repository.get_user_by_phone_number(f" {wpp_user_name}: ")
                #If the sender is in the database, he will be ignored
                if len(find_sender_db) > 0:
                    print('lead already on Firestore.')
                    continue
                #time.sleep(1)
                self.sleepRandom.sleep(1)
                self.move_to_and_click(xy_position=sv["input_send_message_xy"])
                #time.sleep(1)
                self.sleepRandom.sleep(1)


                for message in messages:
                    #self.keyboard.write(message)
                    self.pyautogui.click()
                    #self.pasteMessage(message)
                    self.writeByLetter.write(message)
                    #time.sleep(2)
                    self.sleepRandom.sleep(2)
                    self.pyautogui.hotkey('enter')
                    #time.sleep(2)
                    self.sleepRandom.sleep(2)

                #checking to see if the whatsapp number exists
                extract_messages = ""
                extract_messages = self.get_html.extract_last_messages()

                #if it exists, a new document will be created for the lead
                if len(extract_messages) > 0:
                    now = datetime.now().strftime("%H:%M, %d/%m/%Y")
                    self.repository.insert_new_document(
                        lead=f" {wpp_user_name}: ",
                        message_sender=message_sender,
                        messages = [
                            {
                                "date": now,
                                "sender": message_sender,
                                "text": messages[0]
                            },
                            {
                                "date": now,
                                "sender": message_sender,
                                "text": messages[1]
                            }
                        ],
                        stage=0,
                        created_at=now
                    )

                #time.sleep(1)
                self.sleepRandom.sleep(1)
                self.move_to_and_click(xy_position=sv["input_send_message_xy"])
                self.pyautogui.hotkey('esc')
                line += 1

        with open(self.file_path, 'r', newline='') as csv_file:
            #selecting all the rows but the first 10
            lines = list(csv.reader(csv_file))
            lines = lines[line-1:]

        with open(self.file_path, 'w', newline='') as csv_file:
            #excluding the first 10 phone numbers from the csv file
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(lines)

    def move_to_and_click(self, xy_position):
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        self.pyautogui.click()

    def move_to_and_double_click(self, xy_position):
        #self.pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(self.randomize_time()), tween=self.pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.
        self.bezierMove.move(x2=xy_position[0], y2=  xy_position[1])
        self.pyautogui.doubleClick()

    def randomize_time(self):
        return random.uniform(0.8000, 1.2000)

    def pasteMessage(self, text:str):
        print(f"text: {text}")
        self.pyperclip.copy(text)
        #time.sleep(0.2)
        self.sleepRandom.sleep(0.2)
        self.pyautogui.hotkey('ctrl', 'v')
        #time.sleep(0.2)
        self.sleepRandom.sleep(0.2)
