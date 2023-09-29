#RODAR O TESTE: pytest -s tests/firstMessageTest.py

import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from pathlib import Path
from unittest.mock import MagicMock
from src.scripts.firstMessage.firstMessage import FirstMessage
from .mocks.repositoryMock import repository_mock

base_path = Path(__file__).parents[1].as_posix()
video_path = f"{base_path}/src/videos"
csv_file_path = f"{base_path}/tests/mocks/files/phoneNumbersMock.csv"

def test_send_first_messages_to_correct_number():
    pyautogui_module=MagicMock()
    keyboard_module=MagicMock()
    pyperclip_module=MagicMock()
    get_html=MagicMock()
    repository=repository_mock
    file_path = csv_file_path

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
    repository.get_user_by_name.assert_called()
    repository.insert_new_document.assert_not_called()
