import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
import pyperclip
from src.scripts.firstMessage.firstMessage import FirstMessage
from src.repository.repository import Repository
from src.config import csv_file_path
from src.utils.whatsApp import WhatsApp

is_whatsapp_open = WhatsApp(pyautogui, keyboard, pyperclip).is_whatsapp_open()
if is_whatsapp_open:
    FirstMessage(
        pyautogui, 
        keyboard,
        pyperclip,
        Repository(), 
        csv_file_path
    ).open_conversation()
