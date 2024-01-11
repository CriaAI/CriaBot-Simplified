import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.config import user_name

class UserMessages:
    def get_last_messages(self, all_messages):
        user_last_messages = []

        for message in list(reversed(all_messages)):
            if user_name not in message["sender"]:
                user_last_messages.append(message["text"])
            else:
                break

        user_last_messages = list(reversed(user_last_messages))

        return "\n".join(user_last_messages)