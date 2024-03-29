import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.utils.subprocess import Subprocess
from src.service.pineconeClass import PineconeClass
import uuid
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from src.repository.repository import Repository
from src.utils.userMessages import UserMessages
from src.config import user_name, run_script_extract_messages, run_script_first_message, run_script_send_messages
from src.service.embedModel import embed_model

load_dotenv()

def init():
    st.set_page_config(
        page_title = "Cria.AI ChatBot",
        page_icon = "🤖"
    )
    st.header("ChatBot da Cria.AI 🤖")

def main():
    init()

    users_to_be_answered = Repository().get_users_by_need_to_generate_answer()

    if len(users_to_be_answered) == 0:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Enviar 1ª mensagem", key="script1"):
                st.info("Vá para o whatsapp web COM a aba inspecionar aberta")
                Subprocess(run_script_first_message).run_subprocess()

        with col2:
            if st.button("Extrair mensagens", key="script2"):
                st.info("Vá para o whatsapp web COM a aba inspecionar aberta")
                Subprocess(run_script_extract_messages).run_subprocess()

        with col3:
            if st.button("Responder leads", key="script4"):
                st.info("Vá para o whatsapp web COM a aba inspecionar aberta")
                Subprocess(run_script_send_messages).run_subprocess()

    else:
        doc_id = users_to_be_answered[0].id
        user = users_to_be_answered[0].to_dict()
        all_messages = user["messages"]
        last_messages = UserMessages().get_last_messages(all_messages)



        if user["stage"] == 1:
            with st.sidebar:

                st.info("Baseando-se nas respostas do usuário e da sugestão da IA, como você classifica o lead?")

                col1, col2, col3= st.columns([1, 2, 2])

                with col1:
                    if st.button("bot", key=f"bot_{doc_id}"):
                        data_to_update = {
                            "stage": 0,
                            "q_1": 0,
                            "q_1_text": "bot",
                            "need_to_generate_answer": False,
                            "need_to_send_answer": False,
                            "category": "bot"
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                        st.rerun()

                with col2:
                    if st.button("Não advogado", key=f"not_lawyer_{doc_id}"):
                        data_to_update = {
                            "stage": 0,
                            "q_1": 1,
                            "q_1_text": "nao advogado",
                            "need_to_generate_answer": False,
                            "need_to_send_answer": False,
                            "category": "Not lawyer"
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                        st.rerun()

                with col3:
                    if st.button("Advogado", key=f"lawyer_{doc_id}"):
                        data_to_update = {
                            "stage": 2,
                            "q_1": 2,
                            "q_1_text": "advogado",
                            "need_to_generate_answer": False,
                            "need_to_send_answer": True,
                            "category": "Lawyer"
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                        st.rerun()

                with st.form("response_stage_1"):
                    st.text_area(label="Resposta personalizada", value="", height=200, key="response_stage_1")

                    def handle_submit_stage_1():
                        response = st.session_state.response_stage_1
                        all_messages.append({
                            "date": datetime.now().strftime("%H:%M, %d/%m/%Y"),
                            "sender": user_name,
                            "text": response
                        })

                        data_to_update = {
                            "stage": 1,
                            "q_1": 3,
                            "q_1_text": "mensagem personalizada",
                            "messages": all_messages,
                            "need_to_generate_answer": False,
                            "need_to_send_answer": True,
                            "category": ""
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                    st.form_submit_button("Enviar", on_click=handle_submit_stage_1)

        if user["stage"] == 2:
            with st.sidebar:

                st.info("Baseando-se nas respostas do usuário e da sugestão da IA, como você classifica o interesse do lead?")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Não interessado", key=f"reject_{doc_id}"):
                        data_to_update = {
                            "stage": 0,
                            "q_2": 0,
                            "q_2_text": "nao interessado",
                            "need_to_generate_answer": False,
                            "need_to_send_answer": False
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                        st.rerun()

                with col2:
                    if st.button("Interessado", key=f"accept_{doc_id}"):
                        data_to_update = {
                            "stage": 3,
                            "q_2": 1,
                            "q_2_text": "interessado",
                            "need_to_generate_answer": False,
                            "need_to_send_answer": True
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                        st.rerun()

                with st.form("response_stage_2"):
                    st.text_area(label="Resposta personalizada", value="", height=200, key="response_stage_2")

                    def handle_submit_stage_2():
                        response = st.session_state.response_stage_2
                        all_messages.append({
                            "date": datetime.now().strftime("%H:%M, %d/%m/%Y"),
                            "sender": user_name,
                            "text": response
                        })

                        data_to_update = {
                            "stage": 2,
                            "q_2": 2,
                            "q_2_text": "mensagem personalizada",
                            "messages": all_messages,
                            "need_to_generate_answer": False,
                            "need_to_send_answer": True
                        }
                        Repository().update_user_info(doc_id, data_to_update)
                    st.form_submit_button("Enviar", on_click=handle_submit_stage_2)


        elif user["stage"] == 4:
            st.info("Baseando-se nas respostas do usuário e da sugestão da IA, como você classifica o interesse do lead?")

            with st.sidebar:

                with st.form("my_form"):
                    st.text_area(label="Resposta", value='AI GEN NOT ENABLED!', height=400, key="edited_gpt_answer")#openAIstage4_result["gpt_answer"], height=400, key="edited_gpt_answer")

                    def handle_submit_stage_4():
                        edited_gpt_answer_value = st.session_state.edited_gpt_answer
                        all_messages.append({
                            "date": datetime.now().strftime("%H:%M, %d/%m/%Y"),
                            "sender": user_name,
                            "text": edited_gpt_answer_value
                        })

                        data_to_update = {
                            "messages": all_messages,
                            "q_3": 1,
                            "q_3_text": "mensagem personalizada",
                            "need_to_generate_answer": False,
                            "need_to_send_answer": True
                        }
                        Repository().update_user_info(doc_id, data_to_update)

                    def handle_ignore_stage_4():
                        data_to_update = {
                            "messages": all_messages,
                            "q_3": 0,
                            "need_to_generate_answer": False,
                            "need_to_send_answer": False
                        }
                        Repository().update_user_info(doc_id, data_to_update)

                    st.form_submit_button("Aceitar", on_click=handle_submit_stage_4)
                    st.form_submit_button("Ignorar", on_click=handle_ignore_stage_4)

        # Rendering the message history between the lead and the seller
        for message in all_messages:
            st.info(f"{message['sender']} {message['text']}")


if __name__ == '__main__':
    main()
