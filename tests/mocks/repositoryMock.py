from unittest.mock import MagicMock
class User:
    def __init__(self, id, message_sender, messages, need_to_generate_answer, need_to_send_answer):
        self.id = id
        self.message_sender = message_sender
        self.messages = messages
        self.need_to_generate_answer = need_to_generate_answer
        self.need_to_send_answer = need_to_send_answer

    def to_dict(self):
        return {
            "message_sender": self.message_sender,
            "messages": self.messages,
            "need_to_generate_answer": self.need_to_generate_answer,
            "need_to_send_answer": self.need_to_send_answer
        }


repository_mock = MagicMock()
repository_mock.get_user_by_name.side_effect = lambda message_sender: \
    [User(id="id", message_sender=message_sender, messages=[], need_to_generate_answer=False, need_to_send_answer=False)] \
    if message_sender == " Vittório Girardi: " else []
repository_mock.update_messages_array.side_effect = lambda doc_id, messages: print(f"Mocked update_messages_array({doc_id}, {messages})")
repository_mock.insert_new_document.side_effect = lambda message_sender: print(f"Mocked insert_new_document({message_sender})")
repository_mock.get_users_by_need_to_send_answer.return_value = [
    User(
        id="id1",
        message_sender=" Vittório Girardi: ",
        messages=[{
            "sender": " Vittório Girardi: ",
            "text": "Hello world",
            "date": ""
        }],
        need_to_generate_answer=True,
        need_to_send_answer=True
    )
]
repository_mock.update_need_to_send_answer.side_effect = lambda doc_id: print(f"Mocked update_need_to_send_answer({doc_id})")