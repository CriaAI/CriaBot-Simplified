import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))

import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

from src.databaseConfig.firebaseConfig import users_ref

def init():
    st.set_page_config(
        page_title = "Cria.AI ChatBot",
        page_icon = "🤖"
    )
    st.header("ChatBot da Cria.AI 🤖")

def main():
    load_dotenv()
    init()

    chat = AzureChatOpenAI(
        openai_api_base=os.getenv("BASE_URL"),
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_key=os.getenv("API_KEY"),
        openai_api_type="azure",
    )

    users_to_be_answered = users_ref.where("need_to_generate_answer", "==", True).get()
    
    if len(users_to_be_answered) > 0:
        doc_id = users_to_be_answered[0].id
        user = users_to_be_answered[0].to_dict()
        all_messages = user["messages"]

        #getting all the messages that were sent after the last message the seller sent (CAIO TERÁ QUE MUDAR PARA O NOME DELE)
        #these messages will be used in the gpt prompt
        gpt_prompt = []
        for message in list(reversed(all_messages)):
            if message["sender"] != " Fran Hahn: ":
                gpt_prompt.append(message["text"])
            else:
                break
        
        gpt_prompt = list(reversed(gpt_prompt))

        messages = [
            SystemMessage(content="Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados"),
        ]
        messages.append(HumanMessage(content="\n".join(gpt_prompt)))
    else:
        st.write("Todos os usuários foram respondidos.")
        st.stop()

    with st.sidebar:
        gpt_answer = chat(messages)
        st.info(gpt_answer.content)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Rejeitar", key=f"reject_{doc_id}"):
                gpt_answer = chat(messages)

        with col2:
            if len(users_to_be_answered) > 0:
                if st.button("Aceitar", key=f"accept_{doc_id}"):
                    # Adding the gpt answer to the database
                    all_messages.append({
                        "date": datetime.now().strftime("%H:%M, %d/%m/%Y"),
                        "sender": " Fran Hahn: ", #CAIO, mudar pelo seu nome
                        "text": gpt_answer.content
                    })
                    users_ref.document(doc_id).update({"messages": all_messages})
                    users_ref.document(doc_id).update({"need_to_generate_answer": False})

                    st.experimental_rerun()


    # Rendering the message history between the lead and the seller
    if len(users_to_be_answered) > 0:
        for message in all_messages:
            st.info(f"{message['sender']} {message['text']}")
    
if __name__ == '__main__':
    main()