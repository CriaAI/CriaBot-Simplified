import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyperclip
import pyautogui
from src.repository.repository import Repository
from src.scripts.sendMessages.sendMessages import SendMessages
from src.utils.whatsApp import WhatsApp

is_whatsapp_open = WhatsApp(pyautogui, keyboard, pyperclip).is_whatsapp_open()
if is_whatsapp_open:
    SendMessages(
        pyautogui, 
        keyboard, 
        pyperclip, 
        Repository()
    ).open_conversation()
