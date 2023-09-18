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

def main():
    load_dotenv()

    users_to_be_answered = users_ref.get()
    for user in users_to_be_answered:
        user = user.to_dict()
        print("USER: ", user)

    chat = ChatOpenAI(temperature=0)
    messages = [
        SystemMessage(content="Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados no Brasil"),
    ]
    
    st.set_page_config(
        page_title = "Cria.AI ChatBot",
        page_icon = "🤖"
    )

    st.header("ChatBot da Cria.AI 🤖")

    all_messages = "Aqui estará todo o histórico de mensagens entre o vendedor e o lead"
    st.info(all_messages)

    st.button("Próximo")

    with st.sidebar:
        gpt_answers = "Respostas do chat GPT..."
        st.info(gpt_answers)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Rejeitar"):
                st.write("Você clicou no Botão Rejeitar")
        with col2:
            if st.button("Aceitar"):
                st.write("Você clicou no Botão Aceitar")
        

if __name__ == '__main__':
    main()