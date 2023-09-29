import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
import pyperclip
from src.scripts.firstMessage.firstMessage import FirstMessage
from src.repository.repository import Repository
from src.config import csv_file_path
from src.utils.getHtml import GetHtml

get_whatsapp_title = GetHtml(pyautogui, pyperclip).get_html_from_start_page()

if get_whatsapp_title == "WhatsApp":
    FirstMessage(
        pyautogui, 
        keyboard,
        pyperclip,
        Repository(), 
        csv_file_path
    ).open_conversation()