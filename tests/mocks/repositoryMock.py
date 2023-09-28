import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from unittest.mock import MagicMock
from tests.mocks.usersMock import usersMock, User

repository_mock = MagicMock()

repository_mock.get_user_by_name.side_effect = lambda message_sender: (
    [User(id="id", message_sender=message_sender, messages=[], need_to_generate_answer=False, need_to_send_answer=False, stage=0)]
    if message_sender == " Vittório Girardi: " or message_sender == " Carol Martins: "
    else []
)

repository_mock.get_users_by_need_to_send_answer.return_value = [
    User(
        id="id1",
        message_sender=" Vittório Girardi: ",
        messages=[{
            "sender": " Vittório Girardi: ",
            "text": "Hello world",
            "date": "12:30, 01/09/2023"
        }],
        need_to_generate_answer=False,
        need_to_send_answer=True,
        stage=2
    )
]

repository_mock.get_users_by_need_to_generate_answer.return_value = [
    User(
        id="id2",
        message_sender=" Carol Martins: ",
        messages=[{
            "sender": " Carol Martins: ",
            "text": "Hello world 2",
            "date": "15:00, 02/09/2023"
        }],
        need_to_generate_answer=True,
        need_to_send_answer=False,
        stage=4
    )
]

repository_mock.get_users_by_stage.side_effect = lambda stage: (
    usersMock[0] if stage == 2 else
    usersMock[1] if stage == 4 else
    []
)

repository_mock.update_user_info.side_effect = lambda doc_id, data: print(f"Mocked update_user_info({doc_id}, {data})")

repository_mock.insert_new_document.side_effect = lambda message_sender: print(f"Mocked insert_new_document({message_sender})")
