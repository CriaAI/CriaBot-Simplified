#Arquivo para setar todas as variáveis para rodar os scripts corretamente
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from pathlib import Path
import json

user_name = " Fran Hahn: " #Nome que aparece no whatsapp. Deve ter um espaço antes e depois e os dois pontos

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'setup\screenMapping.json'), 'r', encoding="utf-8") as f:
    screenMapping = json.load(f)

#set variables from json
for element in screenMapping:
    name = element['Name']
    value = element['Value']
    exec(f"{name} = {tuple(value)}")
    print(f"{name} = {tuple(value)}")

filter_box_xy = (464, 235)
first_conversation_box_xy = (212, 400)
first_new_conversation_box_xy = (163, 457)
arrow_inside_conversation_box = (453, 400)
mark_as_unread_option = (544, 573)
input_search_box_xy = (180, 240)
input_search_new_phone_numbers = (175, 302)
input_send_message_xy = (754, 980)
attach_file_xy = (588, 978)
photos_and_videos_xy = (663, 700)
path_to_video_xy = (909, 217)
video_xy = (590, 382)
button_start_new_conversation_xy = (380, 167)
return_button_outside_input_xy = (43, 229)
return_button_inside_input_xy = (41, 238)

base_path = Path(__file__).parents[1].as_posix()
video_path = f"{base_path}/src/videos"
csv_file_path = f"{base_path}/src/files/phoneNumbers.csv"

run_script_extract_messages = f"python {base_path}/src/run/runExtractMessagesScript.py"
run_script_first_message = f"python {base_path}/src/run/runFirstMessageScript.py"
run_script_send_messages = f"python {base_path}/src/run/runSendMessagesScript.py"