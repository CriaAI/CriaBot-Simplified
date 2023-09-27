import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.utils.augmentedPrompt import AugmentedPrompt

load_dotenv()

def openAIstage1(user_last_messages, embed_model):
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

    augmented_prompt = AugmentedPrompt()
    content = augmented_prompt.stage_1(user_last_messages, embed_model)

    gpt_prompt = [
        SystemMessage(content="""Você analisa respostas de leads de um serviço de inteligência artificial que cria documentos 
        para advogados. A sua responsabilidade é classificar os leads como advogado, não advogado ou bot."""),
        HumanMessage(content=content)
    ]

    gpt_answer = chat(gpt_prompt).content

    return gpt_answer