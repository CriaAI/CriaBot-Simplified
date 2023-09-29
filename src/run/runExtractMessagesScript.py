import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import keyboard
import pyautogui
import pyperclip
import time
from src.repository.repository import Repository
from src.scripts.extractMessages.extractMessages import ExtractMessages
from src.utils.getHtml import GetHtml
from src.config import screen_variables as sv

filter_click_type = "click"
previous_sender = ""
sender_to_mark_as_unread = []
get_whatsapp_title = GetHtml(pyautogui, pyperclip).get_html_from_start_page()
i = 0

if get_whatsapp_title == "WhatsApp":
    while i < 10:
        current_sender = ExtractMessages(
            pyautogui,
            pyperclip,
            Repository(),
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
    
    pyautogui.moveTo(sv["filter_box_xy"][0], sv["filter_box_xy"][1], duration=0.5, tween=pyautogui.easeInOutQuad)
    #percorrer lista dos que precisa marcar como não lidos
    for sender in sender_to_mark_as_unread:
        pyautogui.click()
        time.sleep(1)    
        pyautogui.moveTo(sv["input_search_box_xy"][0], sv["input_search_box_xy"][1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        keyboard.write(sender)
        time.sleep(1)
        pyautogui.moveTo(sv["arrow_inside_conversation_box"][0], sv["arrow_inside_conversation_box"][1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(sv["mark_as_unread_option"][0], sv["mark_as_unread_option"][1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(sv["return_button_inside_input_xy"][0], sv["return_button_inside_input_xy"][1], duration=0.5, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        time.sleep(1)
