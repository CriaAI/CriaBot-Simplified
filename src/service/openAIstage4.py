import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

def openAIstage4(user_last_messages):
    chat = AzureChatOpenAI(
        openai_api_base=os.getenv("OPENAI_API_BASE"),
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_type="azure",
        temperature=0.4
    )

    #chat = ChatOpenAI(
    #    openai_api_key=os.getenv("OPENAI_API_KEY"),
    #    model='gpt-3.5-turbo'
    #)

    gpt_prompt = [
        SystemMessage(content="""Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados.
        A empresa que você trabalha se chama Cria.AI e você deve responder as perguntas do lead da melhor forma possível."""),
        HumanMessage(content="\n".join(user_last_messages))
    ]

    gpt_answer = chat(gpt_prompt).content

    return gpt_answer