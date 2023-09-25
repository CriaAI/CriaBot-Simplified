import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

class User:
    def __init__(self, id, message_sender, messages, need_to_generate_answer, need_to_send_answer, stage):
        self.id = id
        self.message_sender = message_sender
        self.messages = messages
        self.need_to_generate_answer = need_to_generate_answer
        self.need_to_send_answer = need_to_send_answer
        self.stage = stage

    def to_dict(self):
        return {
            "message_sender": self.message_sender,
            "messages": self.messages,
            "need_to_generate_answer": self.need_to_generate_answer,
            "need_to_send_answer": self.need_to_send_answer,
            "stage": self.stage
        }

usersMock = [
    {
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
        ),
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
    }
]