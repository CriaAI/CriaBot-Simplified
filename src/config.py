#Arquivo para setar todas as variáveis para rodar os scripts corretamente
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

from pathlib import Path
import json

user_name = "Fran Hahn"

screen_variables = {
    "message_sender_xy": (434, 669),
    "filter_box_xy": (465, 238),
    "first_conversation_box_xy": (230, 393),
    "first_new_conversation_box_xy": (249, 459),
    "arrow_inside_conversation_box": (450, 419),
    "mark_as_unread_option": (558, 662),
    "input_search_box_xy": (171, 240),
    "input_search_new_phone_numbers": (181, 301),
    "input_send_message_xy": (731, 983),
    "attach_file_xy": (587, 977),
    "photos_and_videos_xy": (667, 698),
    "path_to_video_xy": (908, 215),
    "video_xy": (592, 383),
    "button_start_new_conversation_xy": (382, 167),
    "return_button_outside_input_xy": (40, 230),
    "return_button_inside_input_xy": (42, 236)
}

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'setup\screenMapping.json'), 'r', encoding="utf-8") as f:
    screenMapping = json.load(f)

#set variables from json
for element in screenMapping:
    name = element['Name']
    value = element['Value']
    screen_variables[name] = tuple(value)

base_path = Path(__file__).parents[1].as_posix()
video_path = f"{base_path}/src/videos"
csv_file_path = f"{base_path}/src/files/phoneNumbers.csv"

run_script_extract_messages = f"python {base_path}/src/run/runExtractMessagesScript.py"
run_script_first_message = f"python {base_path}/src/run/runFirstMessageScript.py"
run_script_send_messages = f"python {base_path}/src/run/runSendMessagesScript.py"