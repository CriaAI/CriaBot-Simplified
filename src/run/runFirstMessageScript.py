import keyboard

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import pyautogui
from src.scripts.firstMessage.firstMessage import FirstMessage
from src.repository.repository import Repository

FirstMessage(
    pyautogui, 
    keyboard, 
    Repository(), 
    "c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/files/phoneNumbers.csv"
).open_conversation()
