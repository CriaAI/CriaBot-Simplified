#RODAR O TESTE: pytest -s tests/extractMessagesTest.py
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from unittest.mock import MagicMock
from src.scripts.extractMessages.extractMessages import ExtractMessages
from .mocks.repositoryMock import repository_mock
from .mocks.getHtmlFromWhatsAppMock import GetHtmlFromWhatsAppMock
    
def test_open_conversation_from_existing_user_with_html_file():
    pyautogui_module=MagicMock()
    repository=repository_mock
    get_html_from_whatsapp=GetHtmlFromWhatsAppMock()
    filter_click_type="click"

    user = ExtractMessages(
        pyautogui_module=pyautogui_module,
        repository=repository,
        get_html_from_whatsapp=get_html_from_whatsapp,
        filter_click_type=filter_click_type
    ).open_conversation()

    assert user == " Vittório Girardi: "
    assert pyautogui_module.assert_any_call
    repository.get_user_by_name.assert_called()
    repository.update_user_info.assert_called()
    repository.insert_new_document.assert_not_called()

def test_insert_messages_from_existing_user():
    messages = [{'message_text': 'Hello', 'message_sender': ' Vittório Girardi: ', 'message_date': '12:00, 01/10/2023'}]

    pyautogui_module=MagicMock()
    repository=repository_mock
    get_html_from_whatsapp=GetHtmlFromWhatsAppMock()
    filter_click_type="click"

    result = ExtractMessages(
        pyautogui_module=pyautogui_module,
        repository=repository,
        get_html_from_whatsapp=get_html_from_whatsapp,
        filter_click_type=filter_click_type
    ).insert_messages(messages)

    repository.get_user_by_name.assert_called()
    repository.update_user_info.assert_called()
    repository.insert_new_document.assert_not_called()
    assert result == ' Vittório Girardi: '

def test_insert_message_with_no_data_and_cannot_return_error():
    messages = [{'message_text': None, 'message_sender': ' Vittório Girardi: ', 'message_date': '12:00, 01/10/2023'}]

    pyautogui_module=MagicMock()
    repository=repository_mock
    get_html_from_whatsapp=GetHtmlFromWhatsAppMock()
    filter_click_type="click"

    ExtractMessages(
        pyautogui_module=pyautogui_module,
        repository=repository,
        get_html_from_whatsapp=get_html_from_whatsapp,
        filter_click_type=filter_click_type
    ).insert_messages(messages)

    repository.get_user_by_name.assert_called()
    repository.update_user_info.assert_called()
    repository.insert_new_document.assert_not_called()
