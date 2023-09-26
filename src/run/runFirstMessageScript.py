import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
from src.scripts.firstMessage.firstMessage import FirstMessage
from src.repository.repository import Repository
from src.config import csv_file_path

FirstMessage(
    pyautogui, 
    keyboard, 
    Repository(), 
    csv_file_path
).open_conversation()
