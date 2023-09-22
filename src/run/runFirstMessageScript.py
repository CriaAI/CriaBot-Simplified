import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
from src.scripts.firstMessage.firstMessage import FirstMessage
from src.repository.repository import Repository

FirstMessage(pyautogui, keyboard, Repository()).open_conversation()
