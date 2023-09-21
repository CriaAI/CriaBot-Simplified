import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
from src.scripts.firstMessage.firstMessage import FirstMessage

FirstMessage(pyautogui, keyboard).open_conversation()
