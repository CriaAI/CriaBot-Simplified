import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
from src.repository.repository import Repository
from src.scripts.sendMessages.sendMessages import SendMessages

SendMessages(pyautogui, keyboard, Repository()).open_conversation()