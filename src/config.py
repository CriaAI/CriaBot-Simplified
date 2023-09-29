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
    
filter_box_xy = (465, 241) #Botão de filtrar mensagens não lidas no whatsapp
first_conversation_box_xy = (150, 400) #Box da primeira conversa que aparece no whatsapp (conversas existentes)
first_new_conversation_box_xy = (150, 450) #Box da primeira conversa que aparece no whatsapp (conversas novas)
arrow_inside_conversation_box = (455, 410) #Seta dentro da caixa de conversa, logo abaixo da data
mark_as_unread_option = (520, 655) #após clicar no arrow_inside_conversation_box, haverá a opção de marcar como não lido

word_service = (1640, 870) #Localização da palavra serviços que é enviada na primeira mensagem para o lead

input_search_box_xy = (160, 250) #Input para buscar conversas existentes
input_search_new_phone_numbers = (255, 315) #Input para buscar novas conversas
input_send_message_xy = (880, 952) #Input de enviar mensagens

attach_file_xy = (695, 950) #O "+" do conto inferior esquerdo para anexar arquivos/videos/imagens
photos_and_videos_xy = (700, 690) #Após clicar no attach_file_xy, vão aparecer várias opções, e uma delas são fotos e vídeos
path_to_video_xy = (900, 200) #Após clicar em photos_and_videos_xy, queremos clicar na seta para baixo logo ao lado do caminho para o arquivo
video_xy = (600, 400) #Clicar em cima do vídeo

button_start_new_conversation_xy = (475, 198) #Botão do canto superior esquerdo "Nova conversa"
return_button_outside_input_xy = (60, 245) #Ao clicar no botão "Nova conversa", aparece uma seta para retornar para as conversas (deve ser a primeira e a maior que aparece)
return_button_inside_input = (40, 245) #Dentro do input para digitar números, há um pequena seta para retonar


base_path = Path(__file__).parents[1].as_posix()
video_path = f"{base_path}/src/videos"
csv_file_path = f"{base_path}/src/files/phoneNumbers.csv"

run_script_extract_messages = f"python {base_path}/src/run/runExtractMessagesScript.py"
run_script_first_message = f"python {base_path}/src/run/runFirstMessageScript.py"
run_script_send_messages = f"python {base_path}/src/run/runSendMessagesScript.py"