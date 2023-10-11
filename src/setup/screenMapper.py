def elementsToMap():
    return [
        {
            "Name": "profile_picture_xy",
            "Description": "Foto de perfil do usuário",
            "Value":(60, 198)
        },
        {
            "Name":"message_sender_xy",
            "Description": "Botão para editar o nome do usuário",
            "Value":(465, 241)
        },
        {
            "Name":"filter_box_xy",
            "Description": "Botão de filtrar mensagens não lidas no whatsapp",
            "Value":(465, 241)
        },
        {
            "Name":"first_conversation_box_xy",
            "Description": "Box da primeira conversa que aparece no whatsapp (conversas existentes)",
            "Value": (204, 341)
        },
        {
            "Name":"first_new_conversation_box_xy",
            "Description": "Box da primeira conversa que aparece no whatsapp (conversas novas)",
            "Value": (150, 450)
        },
        {
            "Name":"arrow_inside_conversation_box",
            "Description": "Seta dentro do box de conversa",
            "Value": (150, 450)
        },
        {
            "Name":"mark_as_unread_option",
            "Description": "Após clicar na seta dentro do box de conversa, aparecerá a opção de marcar msg como não lida",
            "Value": (150, 450)
        },
        {
            "Name":"input_search_box_xy",
            "Description": "Input para buscar conversas existentes",
            "Value": (160, 250)
        },
        {
            "Name":"input_search_new_phone_numbers",
            "Description": "Input para buscar novas conversas",
            "Value": (255, 315)
        },
        {
            "Name":"input_send_message_xy",
            "Description": "Input de enviar mensagens",
            "Value": (880, 952)
        },
        {
            "Name":"attach_file_xy",
            "Description": "O '+' do conto inferior esquerdo para anexar arquivos/videos/imagens",
            "Value": (695, 950)
        },
        {
            "Name":"photos_and_videos_xy",
            "Description": "Após clicar no attach_file_xy, vão aparecer várias opções, e uma delas são fotos e vídeos",
            "Value": (700, 690)
        },
        {
            "Name":"path_to_video_xy",
            "Description": "Após clicar em photos_and_videos_xy, queremos clicar na seta para baixo logo ao lado do caminho para o arquivo",
            "Value": (900, 200)
        },
        {
            "Name":"video_xy",
            "Description": "Clicar em cima do vídeo",
            "Value": (600, 400)
        },
        {
            "Name":"button_start_new_conversation_xy",
            "Description": "Botão do canto superior esquerdo 'Nova conversa'",
            "Value": (475, 198)
        },
        {
            "Name":"return_button_outside_input_xy",
            "Description": "Ao clicar no botão 'Nova conversa', aparece uma seta para retornar para as conversas (deve ser a primeira e a maior que aparece)",
            "Value": (60, 245)
        },
        {
            "Name":"return_button_inside_input_xy",
            "Description": "Dentro do input para digitar números, há um pequena seta para retonar",
            "Value": (40, 245)
        },
    ]

import keyboard
import pyautogui
import json
import os
class ScreenMapper():
    def __init__(self):
        self.idx = 0
        self.elements = elementsToMap()
        self.waitingPosition = False
        print(len(self.elements))

        print('''
              Mapping position.
              Click Alt to start mapping.
              Click Alt Gr to set mapping point.
              Click Esc to exit.''')
        keyboard.add_hotkey('alt', self.perform_action)
        keyboard.add_hotkey('alt gr', self.perform_action_2)
        keyboard.wait('esc')
    def perform_action(self):
        if self.idx >= (len(self.elements)):
            print('Press ESC to exit!')
            return
        if not self.waitingPosition:
            self.waitingPosition = True
            pyautogui.moveTo(self.elements[self.idx]["Value"])
            print('Mapping position')
            print(f'set value to {self.elements[self.idx]["Name"]}.')
            print(f'{self.elements[self.idx]["Description"]}')
        else:
            print('Click Alt Gr to set position!')
    def perform_action_2(self):
        if self.waitingPosition:
            position = pyautogui.position()
            self.elements[self.idx]["Value"] = (position[0], position[1])
            self.waitingPosition = False
            print('Position set!')
            self.idx += 1
        else:
            print('Click Alt to prepare mouse mapping!')


screenMapper = ScreenMapper()
print(screenMapper.elements)

screenMappingPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'screenMapping.json')
with open(screenMappingPath, "w") as outfile:
    outfile.write(json.dumps(screenMapper.elements))
