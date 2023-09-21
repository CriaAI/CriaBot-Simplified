import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.repository.repository import Repository

load_dotenv()

chat = AzureChatOpenAI(
    openai_api_base=os.getenv("BASE_URL"),
    openai_api_version="2023-05-15",
    deployment_name="gpt-35-turbo",
    openai_api_key=os.getenv("API_KEY"),
    openai_api_type="azure",
    temperature=0.4
)

def init():
    st.set_page_config(
        page_title = "Cria.AI ChatBot",
        page_icon = "🤖"
    )
    st.header("ChatBot da Cria.AI 🤖")

def main():
    init()

    users_to_be_answered = Repository().get_users_by_need_to_generate_answer()

    if len(users_to_be_answered) > 0:
        doc_id = users_to_be_answered[0].id
        user = users_to_be_answered[0].to_dict()
        all_messages = user["messages"]

        #getting all the messages that were sent after the last message the seller sent (CAIO TERÁ QUE MUDAR PARA O NOME DELE)
        #these messages will be used in the gpt prompt
        user_last_messages = []
        for message in list(reversed(all_messages)):
            if message["sender"] != " Fran Hahn: ":
                user_last_messages.append(message["text"])
            else:
                break
        
        user_last_messages = list(reversed(user_last_messages))

        gpt_prompt = [
            SystemMessage(content="""Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados.
            A empresa que você trabalha se chama Cria.AI."""),
            HumanMessage(content="\n".join(user_last_messages))
        ]

        gpt_answer = chat(gpt_prompt).content

        if user["stage"] == 1:
            with st.sidebar:
                st.info("Baseando-se nas respostas do usuário, você quer prosseguir com o envio de mensagens?")

                if st.button("Não", key=f"reject_{doc_id}"):
                    Repository().update_stage_number(doc_id, 0)
                    Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                    Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": False})
                    st.experimental_rerun()

                if st.button("Sim", key=f"accept_{doc_id}"):
                    Repository().update_stage_number(doc_id, 2)
                    Repository().update_need_to_generate_answer(doc_id, {"need_to_generate_answer": False})
                    Repository().update_need_to_send_answer(doc_id, {"need_to_send_answer": True})
                    st.experimental_rerun()
                    
        elif user["stage"] > 3:
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
