#Arquivo para setar todas as variáveis para rodar os scripts corretamente
import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

user_name = " Fran Hahn: " #Nome que aparece no whatsapp. Deve ter um espaço antes e depois e os dois pontos

filter_box_xy = (465, 241) #Botão de filtrar mensagens não lidas no whatsapp
first_conversation_box_xy = (150, 400) #Box da primeira conversa que aparece no whatsapp (conversas existentes)
first_new_conversation_box_xy = (150, 450) #Box da primeira conversa que aparece no whatsapp (conversas novas)
input_search_box_xy = (255, 257) #Input para buscar conversas existentes
input_search_new_phone_numbers = (255, 315) # Input para buscar novas conversas
input_send_message_xy = (880, 952) #Input de enviar mensagens
attach_file_xy = (695, 950) #O "+" do conto inferior esquerdo para anexar arquivos/videos/imagens
photos_and_videos_xy = (700, 690) #Após clicar no attach_file_xy, vão aparecer várias opções, e uma delas são fotos e vídeos
path_to_video_xy = (900, 200) #Após clicar em photos_and_videos_xy, queremos clicar na seta para baixo logo ao lado do caminho para o arquivo
video_xy = (600, 400) #Clicar em cima do vídeo
button_start_new_conversation_xy = (475, 198) #Botão do canto superior esquerdo "Nova conversa"
return_button_xy = (60, 245) #Ao clicar no botão "Nova conversa", aparece uma seta para retornar para as conversas (deve ser a primeira e a maior que aparece)

#Esse video está dentro da pasta videos. Arrumar o caminho de acordo com o seu pc
#ATENÇÃO: não adicionar o arquivo do vídeo, apenas a pasta
video_path = "c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/videos"

#dentro da pasta files há um arquivo csv. Arrumar de acordo com o seu pc
csv_file_path = "c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/files/phoneNumbers.csv"

#Esses são os caminhos para que possamos rodar os scripts. Arrumar de acordo com o seu pc
run_script_extract_messages = "python c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/run/runExtractMessagesScript.py"
run_script_first_message = "python c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/run/runFirstMessageScript.py"
run_script_send_messages = "python c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/run/runSendMessagesScript.py"