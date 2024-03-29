import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from .userMock import User

list_of_users_mock = [
    User(
        id="id1",
        message_sender="Fran Hahn",
        lead=" Vittório Girardi: ",
        messages=[{
            "sender": " Vittório Girardi: ",
            "text": "Hello world",
            "date": "12:30, 01/09/2023"
        }],
        need_to_generate_answer=False,
        need_to_send_answer=True,
        stage=2,
        category="Lawyer",
        created_at="16:14, 01/10/2023"
    ),
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
        created_at="16:14, 02/10/2023"
    )
]