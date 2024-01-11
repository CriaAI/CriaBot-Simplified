import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
from src.utils.bezier_move import BezierMove
from src.utils.write_by_letter import WriteByLetter
from src.utils.sleep_random import SleepRandom
import pyperclip
import pygetwindow as gw
from src.scripts.firstMessage.firstMessage import FirstMessage
from src.repository.repository import Repository
from src.config import csv_file_path
from src.utils.getHtml import GetHtml

print('starting')
get_whatsapp_title = GetHtml(pyautogui, pyperclip, BezierMove()).get_html_from_start_page()
print(get_whatsapp_title)
if get_whatsapp_title is not None and "WhatsApp" in get_whatsapp_title:
    all_windows = gw.getWindowsWithTitle('')

    for window in all_windows:
        if "WhatsApp" in window.title:
            window.activate()
            FirstMessage(
                pyautogui,
                keyboard,
                pyperclip,
                GetHtml(pyautogui, pyperclip, BezierMove()),
                Repository(),
                csv_file_path,
                BezierMove(),
                WriteByLetter(),
                SleepRandom()
            ).open_conversation()
