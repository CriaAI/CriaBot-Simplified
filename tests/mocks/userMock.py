import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

class User:
    def __init__(self, id, message_sender, messages, need_to_generate_answer, need_to_send_answer, stage, category):
        self.id = id
        self.message_sender = message_sender
        self.messages = messages
        self.need_to_generate_answer = need_to_generate_answer
        self.need_to_send_answer = need_to_send_answer
        self.stage = stage
        self.category = category

    def to_dict(self):
        return {
            "message_sender": self.message_sender,
            "messages": self.messages,
            "need_to_generate_answer": self.need_to_generate_answer,
            "need_to_send_answer": self.need_to_send_answer,
            "stage": self.stage,
            "category": self.category
        }