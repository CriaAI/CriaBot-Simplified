import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import keyboard
import pyautogui
import pyperclip
import time
from src.repository.repository import Repository
from src.scripts.extractMessages.extractMessages import ExtractMessages
from src.scripts.extractMessages.getHtmlFromWhatsApp import GetHtmlFromWhatsApp
from src.utils.whatsApp import WhatsApp
from src.config import input_search_box_xy, return_button_inside_input, arrow_inside_conversation_box, mark_as_unread_option

filter_click_type = "click"
previous_sender = ""
sender_to_mark_as_unread = []
is_whatsapp_open = WhatsApp(pyautogui, keyboard, pyperclip).is_whatsapp_open()
i = 0

if is_whatsapp_open:
    while i < 10:
        current_sender = ExtractMessages(
            pyautogui,
            Repository(),
            GetHtmlFromWhatsApp(pyautogui, pyperclip),
            filter_click_type
        ).open_conversation()

        if not isinstance(current_sender, str):
            sender_to_mark_as_unread.append(current_sender["sender"])

        if filter_click_type == "click":
            filter_click_type = "double_click"

        #This is to avoid an infinite loop
        if previous_sender == current_sender:
            break

        previous_sender = current_sender
        i += 1
    
    #percorrer lista dos que precisa marcar como não lidos
    for sender in sender_to_mark_as_unread:
        pyautogui.moveTo(input_search_box_xy[0], input_search_box_xy[1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        keyboard.write(sender)
        time.sleep(1)
        pyautogui.moveTo(arrow_inside_conversation_box[0], arrow_inside_conversation_box[1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(mark_as_unread_option[0], mark_as_unread_option[1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(return_button_inside_input[0], return_button_inside_input[1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
