import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.service.openAIstage1 import openAIstage1
from src.service.openAIstage2 import openAIstage2
from src.service.openAIstage4 import openAIstage4
import streamlit as st
from datetime import datetime
from src.repository.repository import Repository
from src.utils.subprocess import Subprocess
from src.utils.userLastMessages import UserMessages
from src.config import user_name, run_script_extract_messages, run_script_first_message, run_script_send_messages

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
                st.info("Vá para o whatsapp web SEM A ABA DE INSPECIONAR ABERTA em até 4 segundos")
                Subprocess(run_script_first_message).run_subprocess()
                    
        with col2:
            if st.button("Extrair mensagens", key="script2"):
                st.info("Vá para o whatsapp web COM A ABA DE INSPECIONAR ABERTA em até 4 segundos")
                Subprocess(run_script_extract_messages).run_subprocess()

        with col3:
            if st.button("Responder leads", key="script4"):
                st.info("Vá para o whatsapp web SEM A ABA DE INSPECIONAR ABERTA em até 4 segundos")
                Subprocess(run_script_send_messages).run_subprocess()
    else:
        doc_id = users_to_be_answered[0].id
        user = users_to_be_answered[0].to_dict()
        all_messages = user["messages"]
        last_messages = UserMessages().get_last_messages(all_messages)

        if user["stage"] < 3:
            with st.sidebar:
                gpt_suggestion = ""

                if user["stage"] == 1:
                    gpt_suggestion = openAIstage1(last_messages)
                elif user["stage"] == 2:
                    gpt_suggestion = openAIstage2(last_messages)

                st.info("Baseando-se nas respostas do usuário e da sugestão da IA, você quer prosseguir com o envio de mensagens?")
                st.info(gpt_suggestion)

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Rejeitar", key=f"reject_{doc_id}"):
                        Repository().update_stage_number(doc_id, 0)
                        Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                        Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": False})
                        st.experimental_rerun()

                with col2:
                    if st.button("Aceitar", key=f"accept_{doc_id}"):
                        Repository().update_stage_number(doc_id, user["stage"] + 1)
                        Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                        Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": True})
                        st.experimental_rerun()
                        
        elif user["stage"] > 3:
            gpt_answer = openAIstage4(last_messages)

            with st.sidebar:
                with st.form("my_form"):
                    st.text_area(label="Resposta", value=gpt_answer, height=400, key="edited_gpt_answer")

                    def handle_submit():
                        edited_gpt_answer_value = st.session_state.edited_gpt_answer
                        all_messages.append({
                            "date": datetime.now().strftime("%H:%M, %d/%m/%Y"),
                            "sender": user_name,
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

    
if __name__ == '__main__':
    main()
