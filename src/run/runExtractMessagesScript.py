import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import keyboard
import pyautogui
import pyperclip
from src.repository.repository import Repository
from src.scripts.extractMessages.extractMessages import ExtractMessages
from src.scripts.extractMessages.getHtmlFromWhatsApp import GetHtmlFromWhatsApp
from src.utils.whatsApp import WhatsApp

filter_click_type = "click"
previous_sender = ""
is_whatsapp_open = WhatsApp(pyautogui, keyboard, pyperclip).is_whatsapp_open()

if is_whatsapp_open:
    while True:
        current_sender = ExtractMessages(
            pyautogui,
            Repository(),
            GetHtmlFromWhatsApp(pyautogui, pyperclip),
            filter_click_type
        ).open_conversation()

        if filter_click_type == "click":
            filter_click_type = "double_click"

        #This is to avoid an infinite loop
        if previous_sender == current_sender:
            break

        previous_sender = current_sender
