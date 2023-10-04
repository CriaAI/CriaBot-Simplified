import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

class User:
    def __init__(self, id, lead, message_sender, messages, need_to_generate_answer, need_to_send_answer, stage, category, created_at):
        self.id = id
        self.lead = lead
        self.message_sender = message_sender
        self.messages = messages
        self.need_to_generate_answer = need_to_generate_answer
        self.need_to_send_answer = need_to_send_answer
        self.stage = stage
        self.category = category
        self.created_at = created_at

    def to_dict(self):
        return {
            "lead": self.lead,
            "message_sender": self.message_sender,
            "messages": self.messages,
            "need_to_generate_answer": self.need_to_generate_answer,
            "need_to_send_answer": self.need_to_send_answer,
            "stage": self.stage,
            "category": self.category,
            "created_at": self.created_at
        }