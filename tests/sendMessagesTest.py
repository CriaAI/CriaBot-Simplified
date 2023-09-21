#RODAR O TESTE: pytest -s tests/sendMessagesTest.py
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from unittest.mock import MagicMock
from src.scripts.sendMessages.sendMessages import SendMessages
from mocks.repositoryMock import repository_mock

def test_open_conversation():
    pyautogui_module=MagicMock()
    keyboard_module=MagicMock()
    repository=repository_mock
    
    SendMessages(
        pyautogui_module=pyautogui_module,
        keyboard_module=keyboard_module,
        repository=repository
    ).open_conversation()

    assert pyautogui_module.assert_any_call
    assert keyboard_module.assert_any_call
    assert repository.assert_has_calls
