#RODAR O TESTE: pytest -s tests/firstMessageTest.py

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import csv
from pathlib import Path
from unittest.mock import MagicMock
from src.scripts.firstMessage.firstMessage import FirstMessage
from .mocks.repositoryMock import repository_mock

base_path = Path(__file__).parents[1].as_posix()
video_path = f"{base_path}/src/videos"
csv_file_path = f"{base_path}/tests/mocks/files/phoneNumbersMock.csv"

def test_send_first_messages_to_whatsapp_numbers_that_dont_exist():
    pyautogui_module=MagicMock()
    keyboard_module=MagicMock()
    pyperclip_module=MagicMock()
    get_html=MagicMock()
    repository=repository_mock
    file_path = csv_file_path

    #adding phone nubers to the csv file
    phone_numbers = ["51 99999999-9999", "51 998888-0000000"]

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        for phone in phone_numbers:
            writer.writerow([phone])

    FirstMessage(
        pyautogui_module=pyautogui_module,
        keyboard_module=keyboard_module,
        pyperclip_module=pyperclip_module,
        get_html=get_html,
        repository=repository,
        file_path=file_path
    ).open_conversation()

    assert pyautogui_module.assert_any_call
    assert keyboard_module.assert_any_call
    assert pyperclip_module.assert_any_call
    repository.get_user_by_phone_number.assert_called()
    repository.insert_new_document.assert_not_called()

def test_send_first_messages_to_whatsapp_numbers_that_exist():
    pyautogui_module=MagicMock()
    keyboard_module=MagicMock()
    pyperclip_module=MagicMock()
    get_html=MagicMock()
    get_html.extract_last_messages.return_value = ["message1", "message2"] #pretending the whatsapp numbers exist
    repository=repository_mock
    file_path = csv_file_path

    #adding phone nubers to the csv file
    phone_numbers = ["51 99336-1676", "51 99556-8965"]

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        for phone in phone_numbers:
            writer.writerow([phone])

    FirstMessage(
        pyautogui_module=pyautogui_module,
        keyboard_module=keyboard_module,
        pyperclip_module=pyperclip_module,
        get_html=get_html,
        repository=repository,
        file_path=file_path
    ).open_conversation()

    assert pyautogui_module.assert_any_call
    assert keyboard_module.assert_any_call
    assert pyperclip_module.assert_any_call
    repository.get_user_by_phone_number.assert_called()
    repository.insert_new_document.assert_called()
