import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

def user_last_messages(all_messages):
    user_last_messages = []
    
    for message in list(reversed(all_messages)):
        if message["sender"] != " Fran Hahn: ": #CAIO mudar pelo teu nome
            user_last_messages.append(message["text"])
        else:
            break
    
    user_last_messages = list(reversed(user_last_messages))

    return user_last_messages