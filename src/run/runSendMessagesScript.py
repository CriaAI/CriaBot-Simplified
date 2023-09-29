import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyperclip
import pyautogui
from src.repository.repository import Repository
from src.scripts.sendMessages.sendMessages import SendMessages
from src.utils.getHtml import GetHtml

get_whatsapp_title = GetHtml(pyautogui, pyperclip).get_html_from_start_page()

if get_whatsapp_title == "WhatsApp":
    SendMessages(
        pyautogui, 
        keyboard, 
        pyperclip, 
        Repository()
    ).open_conversation()
