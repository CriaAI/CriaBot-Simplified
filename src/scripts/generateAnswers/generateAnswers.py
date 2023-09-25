import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import streamlit as st
from datetime import datetime
from src.repository.repository import Repository
from src.service.openAI import openAI
import subprocess

def init():
    st.set_page_config(
        page_title = "Cria.AI ChatBot",
        page_icon = "🤖"
    )
    st.header("ChatBot da Cria.AI 🤖")

def main():
    init()

    users_to_be_answered = Repository().get_users_by_need_to_generate_answer()

    def run_subprocess(script):
        process = subprocess.Popen(script, shell=True, stderr=subprocess.PIPE)
        process.wait()
        stderr = process.stderr.read().decode('utf-8')

        if process.returncode != 0:
            st.error(f"Ocorreu um erro: {stderr}")
        else:
            st.success("Script executado com sucesso!")        

    if len(users_to_be_answered) == 0:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Enviar 1ª mensagem", key="script1"):
                st.info("Vá para o whatsapp web SEM A ABA DE INSPECIONAR ABERTA em até 4 segundos")

                #CAIO mudar pelo caminho no teu pc
                run_subprocess("python c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/run/runFirstMessageScript.py")
        
        with col2:
            if st.button("Extrair mensagens", key="script2"):
                st.info("Vá para o whatsapp web COM A ABA DE INSPECIONAR ABERTA em até 4 segundos")
                
                #CAIO mudar pelo caminho no teu pc
                run_subprocess("python c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/run/runExtractMessagesScript.py")

        with col3:
            if st.button("Responder leads", key="script4"):
                st.info("Vá para o whatsapp web SEM A ABA DE INSPECIONAR ABERTA em até 4 segundos")

                #CAIO mudar pelo caminho no teu pc
                run_subprocess("python c:/Users/fran_/Documents/EMPRESA/CRIA.AI/CriaBot/src/run/runSendMessagesScript.py")

    else:
        if len(users_to_be_answered) > 0:
            doc_id = users_to_be_answered[0].id
            user = users_to_be_answered[0].to_dict()
            all_messages = user["messages"]

            if user["stage"] < 3:
                with st.sidebar:
                    st.info("Baseando-se nas respostas do usuário, você quer prosseguir com o envio de mensagens?")

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("Não", key=f"reject_{doc_id}"):
                            Repository().update_stage_number(doc_id, 0)
                            Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                            Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": False})
                            st.experimental_rerun()

                    with col2:
                        if st.button("Sim", key=f"accept_{doc_id}"):
                            Repository().update_stage_number(doc_id, user["stage"] + 1)
                            Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                            Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": True})
                            st.experimental_rerun()
                            
            elif user["stage"] > 3:
                #getting all the messages that were sent after the last message the seller sent (CAIO TERÁ QUE MUDAR PARA O NOME DELE)
                #these messages will be used in the gpt prompt
                user_last_messages = []
                for message in list(reversed(all_messages)):
                    if message["sender"] != " Fran Hahn: ":
                        user_last_messages.append(message["text"])
                    else:
                        break
                
                user_last_messages = list(reversed(user_last_messages))
                gpt_answer = openAI(user_last_messages)

                with st.sidebar:
                    with st.form("my_form"):
                        st.text_area(label="Resposta", value=gpt_answer, height=400, key="edited_gpt_answer")

                        def handle_submit():
                            edited_gpt_answer_value = st.session_state.edited_gpt_answer
                            all_messages.append({
                                "date": datetime.now().strftime("%H:%M, %d/%m/%Y"),
                                "sender": " Fran Hahn: ", #CAIO, mudar pelo seu nome
                                "text": edited_gpt_answer_value
                            })

                            Repository().update_messages_array(doc_id, all_messages)
                            Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                            Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": True})

                        st.form_submit_button("Aceitar", on_click=handle_submit)
                        
                    if st.button("Rejeitar", key=f"reject_{doc_id}"):
                        print("REJECTED GPT MESSAGE")
                        
            # Rendering the message history between the lead and the seller
            for message in all_messages:
                st.info(f"{message['sender']} {message['text']}")

        else:
            st.write("Todos os usuários foram respondidos.")
            st.stop()
    
if __name__ == '__main__':
    main()
