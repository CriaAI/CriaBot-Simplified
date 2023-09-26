#RODAR O TESTE: pytest -s tests/firstMessageTest.py

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from unittest.mock import MagicMock
from src.scripts.firstMessage.firstMessage import FirstMessage
from mocks.repositoryMock import repository_mock

def test_send_first_messages_to_correct_number():
    pyautogui_module=MagicMock()
    keyboard_module=MagicMock()
    repository=repository_mock
    file_path = "c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/tests/mocks/files/phoneNumbersMock.csv"

    FirstMessage(
        pyautogui_module=pyautogui_module,
        keyboard_module=keyboard_module,
        repository=repository,
        file_path=file_path
    ).open_conversation()

    assert pyautogui_module.assert_any_call
    assert keyboard_module.assert_any_call
    repository.get_user_by_name.assert_called_once()
    repository.insert_new_document.assert_called_once()
