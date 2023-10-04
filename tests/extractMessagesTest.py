#RODAR O TESTE: pytest -s tests/extractMessagesTest.py
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from datetime import datetime
from unittest.mock import MagicMock
from src.scripts.extractMessages.extractMessages import ExtractMessages
from .mocks.repositoryMock import repository_mock

def test_insert_messages_from_existing_user():
    messages = [{"message_text": "Hello", "message_sender": " Vittório Girardi: ", "message_date": "12:00, 01/09/2023"}]

    pyautogui_module=MagicMock()
    pyperclip_module=MagicMock()
    repository=repository_mock
    filter_click_type="click"

    result = ExtractMessages(
        pyautogui_module=pyautogui_module,
        pyperclip_module=pyperclip_module,
        repository=repository,
        filter_click_type=filter_click_type
    ).insert_messages(messages)

    repository.get_user_by_phone_number.assert_called()
    repository.update_user_info.assert_called()
    repository.insert_new_document.assert_not_called()
    assert result == " Vittório Girardi: "

def test_insert_messages_from_new_user():
    messages = [{"message_text": "Hello", "message_sender": " New User: ", "message_date": "12:00, 01/09/2023"}]
    
    pyautogui_module=MagicMock()
    pyperclip_module=MagicMock()
    repository=repository_mock
    filter_click_type="click"

    user = ExtractMessages(
        pyautogui_module=pyautogui_module,
        pyperclip_module=pyperclip_module,
        repository=repository,
        filter_click_type=filter_click_type
    ).insert_messages(messages)

    assert user == " New User: "
    assert pyautogui_module.assert_any_call
    repository.get_user_by_phone_number.assert_called()
    repository.update_user_info.assert_called()
    repository.insert_new_document.assert_called()

def test_insert_message_with_no_data_and_cannot_return_error():
    messages = [{"message_text": None, "message_sender": " Vittório Girardi: ", "message_date": "12:00, 01/09/2023"}]

    pyautogui_module=MagicMock()
    pyperclip_module=MagicMock()
    repository=repository_mock
    filter_click_type="click"

    ExtractMessages(
        pyautogui_module=pyautogui_module,
        pyperclip_module=pyperclip_module,
        repository=repository,
        filter_click_type=filter_click_type
    ).insert_messages(messages)

    repository.get_user_by_phone_number.assert_called()
    repository.update_user_info.assert_called()

def test_insert_messages_from_existing_user_which_the_last_message_was_sent_less_than_5min_ago():
    now = datetime.now()
    messages = [{"message_text": "Hello", "message_sender": " Vittório Girardi: ", "message_date": now.strftime('%H:%M, %d/%m/%Y')}]

    pyautogui_module=MagicMock()
    pyperclip_module=MagicMock()
    repository=repository_mock
    filter_click_type="click"

    result = ExtractMessages(
        pyautogui_module=pyautogui_module,
        pyperclip_module=pyperclip_module,
        repository=repository,
        filter_click_type=filter_click_type
    ).insert_messages(messages)

    repository.get_user_by_phone_number.assert_called()
    assert result["sender"] == "Vittório Girardi"