from src.databaseConfig.firebaseConfig import users_ref

class Repository:
    def get_user_by_phone_number(self, sender_phone):
        return users_ref.where("lead", "==", sender_phone).get()

    def get_users_by_need_to_send_answer(self, message_sender):
        users = users_ref.where("need_to_send_answer", "==", True).where("message_sender", "==", message_sender).get()
        return users

    def get_users_by_need_to_generate_answer(self):
        users = users_ref.where("need_to_generate_answer", "==", True).get()
        return users

    def get_users_by_stage(self, stage_number):
        users = users_ref.where("stage", "==", stage_number).get()
        return users

    def get_all_users(self):
        users_stream = users_ref.stream()
        return users_stream

    def update_user_info(self, doc_id, data):
        users_ref.document(doc_id).update(data)

    def insert_new_document(self, lead, message_sender, stage, messages, created_at):
        users_ref.add({
            "lead": lead,
            "message_sender": message_sender,
            "stage": stage,
            "category": "",
            "need_to_generate_answer": False,
            "need_to_send_answer": False,
            "messages": messages,
            "created_at": created_at
        })
