import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from unittest.mock import MagicMock
from .userMock import User
from .listOfUsersMock import list_of_users_mock
from unittest.mock import MagicMock

class RepositoryMock:
    def insert_new_document(self, lead, messages, created_at, stage, message_sender="Fran Hahn"):
        new_user = User(
            id="id3", 
            lead=lead,
            message_sender=message_sender, 
            messages=messages,
            need_to_generate_answer=False, 
            need_to_send_answer=False, 
            stage=stage,
            category="",
            created_at=created_at
        )
        list_of_users_mock.append(new_user)

    def get_user_by_phone_number(self, message_sender):
        for user in list_of_users_mock:
            if user.message_sender == message_sender:
                return [user]
        return []
    
    def get_users_by_need_to_send_answer(self, username):
        return [list_of_users_mock[0]]
    
    def get_users_by_need_to_generate_answer(self):
        return [list_of_users_mock[1]]
    
    def get_users_by_stage(self, stage_number):
        for user in list_of_users_mock:
            if user.stage == stage_number:
                return [user]
        return []
    
    def update_user_info(self, doc_id, data):
        print(f"User info method called for user id {doc_id}.")


repository_mock = MagicMock(spec=RepositoryMock)

repository_mock.get_user_by_phone_number.side_effect = lambda lead: [
    user for user in list_of_users_mock if user.lead == lead
]

repository_mock.insert_new_document.side_effect = lambda lead, stage, messages, created_at, message_sender="Fran Hahn": list_of_users_mock.append(
    User(
        id="id3", 
        lead=lead,
        message_sender=message_sender, 
        messages=messages, 
        need_to_generate_answer=False, 
        need_to_send_answer=False, 
        stage=stage,
        category="",
        created_at=created_at
    )
)

repository_mock.get_users_by_need_to_send_answer.side_effect = lambda message_sender: [
    User(
        id="id1",
        lead=" Vittório Girardi: ",
        message_sender="Fran Hahn",
        messages=[{
            "sender": " Vittório Girardi: ",
            "text": "Hello world",
            "date": "12:30, 01/09/2023"
        }],
        need_to_generate_answer=False,
        need_to_send_answer=True,
        stage=2,
        category="Lawyer",
        created_at="16:14, 03/10/2023"
    )
]

repository_mock.get_users_by_need_to_generate_answer.return_value = [
    User(
        id="id2",
        message_sender="Fran Hahn",
        lead=" Carol Martins: ",
        messages=[{
            "sender": " Carol Martins: ",
            "text": "Hello world 2",
            "date": "15:00, 02/09/2023"
        }],
        need_to_generate_answer=True,
        need_to_send_answer=False,
        stage=4,
        category="Lawyer",
        created_at="16:14, 03/10/2023"
    )
]

repository_mock.get_users_by_stage.side_effect = lambda stage: (
    list_of_users_mock[0] if stage == 2 else
    list_of_users_mock[1] if stage == 4 else
    []
)

repository_mock.update_user_info.side_effect = lambda doc_id, data: print(f"Mocked update_user_info({doc_id}, {data})")