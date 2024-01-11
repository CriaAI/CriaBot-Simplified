import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))
import re
import pandas as pd
from src.repository.repository import Repository
from src.utils.bezier_move import BezierMove
repository = Repository()
from src.utils.getHtml import GetHtml
import pyautogui, pyperclip, random, time, re
from src.config import screen_variables as sv

#all_users = db.collection("users").stream()



def get_lead_name(lead):
    move_to_and_click(xy_position = sv["input_search_box_xy"])
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)
    pyautogui.write(lead)
    time.sleep(1)
    move_to_and_click(xy_position=sv["first_conversation_box_xy"])
    time.sleep(2)
    wpp_user = get_html.extract_user()
    return wpp_user

def move_to_and_click(xy_position):
    pyautogui.moveTo(xy_position[0], xy_position[1], duration=0.5*(randomize_time()), tween=pyautogui.easeInOutQuad)
    pyautogui.click()

def randomize_time():
    return random.uniform(0.8000, 1.2000)

def update_lead_name():
    userStream = repository.get_all_users()
    for user in userStream:
        user_id = user.id
        user_data = user.to_dict()
        lead = user_data['lead']
        #get lead text
        df = pd.concat([df, pd.DataFrame({'lead_old':lead}, index=[0])], ignore_index = True)
        if not '+' in lead:
            #print(user_id)
            phone_number = re.sub(r'[^0-9]+', '', lead)
            if phone_number[4] in ['3', '2']:
                phone_number_fixed = f" +{phone_number[:2]} {phone_number[2:4]} {phone_number[4:8]}-{phone_number[8:]}: "
            else:
                phone_number_fixed = f" +{phone_number[:2]} {phone_number[2:4]} {phone_number[5:9]}-{phone_number[9:]}: "
            #print(phone_number_fixed)
            repository.update_user_info(user_id, {"lead": phone_number_fixed})

def save_all_lead():
    userStream = repository.get_all_users()
    df = pd.DataFrame(columns = ['id', 'lead'])
    for user in userStream:
        user_id = user.id
        user_data = user.to_dict()
        lead = user_data['lead']
        df = pd.concat([df, pd.DataFrame({'id': user_id, 'lead':lead}, index=[0])], ignore_index = True)
    df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads.csv'), index = False)
'''def get_all_lead_name():
    #userStream = repository.get_all_users()
    userStream = ['554797294342']
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads.csv'))
    for user in userStream:
        #user_id = row['id']
        #user_data = user.to_dict()
        lead = user
        #get lead whatsapp name
        lead_numbers = re.sub(r'[^0-9]+', '', lead)
        lead_wpp_name = get_lead_name(lead_numbers)
        #print(f"user_id: {user_id}")
        print(f"lead_wpp_name: {lead_wpp_name}")
        #if not ("None" in lead_wpp_name):
            #repository.update_user_info(user_id, {"lead": lead_wpp_name})
'''
def get_all_lead_name():
    #userStream = repository.get_all_users()
    #userStream = ['+55 12 99651-9112', '+55 12 99161-6094']
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads.csv'))
    for index, row in df.iterrows():
        user_id = row['id']
        #user_data = user.to_dict()
        lead = row['lead']
        #get lead whatsapp name
        lead_numbers = re.sub(r'[^0-9]+', '', lead)
        lead_numbers = lead_numbers[4:]
        lead_wpp_name = get_lead_name(lead_numbers)
        #print(f"user_id: {user_id}")
        print(f"lead_wpp_name: {lead_wpp_name}")
        if not ("None" in lead_wpp_name):
            repository.update_user_info(user_id, {"lead": lead_wpp_name})

df = pd.DataFrame(columns=['lead_old'])
get_html = GetHtml(pyautogui, pyperclip, BezierMove())
time.sleep(3)
get_all_lead_name()
#print(os.path.join(os.path.abspath(os.curdir), 'leads.csv'))
#print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'leads.csv'))
#save_all_lead()
