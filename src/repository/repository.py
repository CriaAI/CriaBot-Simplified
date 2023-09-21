from src.databaseConfig.firebaseConfig import users_ref

class Repository:
    def get_user_by_name(self, sender):
        return users_ref.where("message_sender", "==", sender).get()
    
    def update_messages_array(self, doc_id, messages):
        users_ref.document(doc_id).update({"messages": messages})

    def insert_new_document(self, message_sender):
        users_ref.add({
            "message_sender": message_sender,
            "stage": 1,
            "need_to_generate_answer": True,
            "need_to_send_answer": True,
            "messages": []
        })

    def get_users_by_need_to_send_answer(self):
        users = users_ref.where("need_to_send_answer", "==", True).get()
        return users
    
    def get_users_by_need_to_generate_answer(self):
        users = users_ref.where("need_to_generate_answer", "==", True).get()
        return users

    def update_need_to_send_answer(self, doc_id, object):
        users_ref.document(doc_id).update(object)

    def update_need_to_generate_answer(self, doc_id, object):
        users_ref.document(doc_id).update(object)
    