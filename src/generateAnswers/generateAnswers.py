import sys,os
sys.path.insert(0, os.path.abspath(os.curdir))
import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

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

    chat = ChatOpenAI(temperature=0.5)

    i = 0
    users_to_be_answered = users_ref.where("messages", "array_contains", {"was_answered": False}).get()
    print("USERS: ", users_to_be_answered)

    if i < len(users_to_be_answered):
        user = users_to_be_answered[i].to_dict()
        all_messages = user["messages"]

        #filtering the messages that are not from the seller (CAIO TERÁ QUE MUDAR PARA O NOME DELE)
        #and that have not been answered yet
        def filter_messages(message):
            if message["sender"] != " Fran Hahn: " and message["was_answered"] == False:
                return message

        filter_messages = list(filter(filter_messages, all_messages))
        gpt_prompt = []
        for message in filter_messages:
            gpt_prompt.append(message["text"])
        
        messages = [
            SystemMessage(content="Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados no Brasil"),
        ]
        messages.append(HumanMessage(content="\n".join(gpt_prompt)))
    else:
        st.write("Todos os usuários foram respondidos.")

    with st.sidebar:
        gpt_answer = chat(messages)
        st.info(gpt_answer.content)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Rejeitar", key=f"reject_{i}"):
                gpt_answer = chat(messages)

        with col2:
            if i < len(users_to_be_answered):
                if st.button("Aceitar", key=f"accept_{i}"):
                    st.write("Você clicou no Botão Aceitar")
                    # Injetar a resposta no banco de dados
                    # Fazer um update de todas as mensagens para was_answered: true
                    i += 1

    # Rendering the message history between the lead and the seller
    if i < len(users_to_be_answered):
        for message in all_messages:
            st.info(f"{message['sender']} {message['text']}")
    

if __name__ == '__main__':
    main()