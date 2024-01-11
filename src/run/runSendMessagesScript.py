import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyperclip
import pyautogui
import pygetwindow as gw
from src.repository.repository import Repository
from src.scripts.sendMessages.sendMessages import SendMessages
from src.utils.bezier_move import BezierMove
from src.utils.getHtml import GetHtml

get_whatsapp_title = GetHtml(pyautogui, pyperclip, BezierMove()).get_html_from_start_page()

if get_whatsapp_title is not None and "WhatsApp" in get_whatsapp_title:
    all_windows = gw.getWindowsWithTitle('')

    for window in all_windows:
        if "WhatsApp" in window.title:
            window.activate()

            SendMessages(
                pyautogui,
                keyboard,
                pyperclip,
                BezierMove(),
                Repository()
            ).open_conversation()
