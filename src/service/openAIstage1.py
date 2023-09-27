import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.utils.augmentedPrompt import AugmentedPrompt

load_dotenv()

def openAIstage1(user_last_messages):
    chat = AzureChatOpenAI(
        openai_api_base=os.getenv("BASE_URL"),
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_key=os.getenv("API_KEY"),
        openai_api_type="azure",
        temperature=0.4
    )

    augmented_prompt = AugmentedPrompt()
    content = augmented_prompt.stage_1(user_last_messages)

    gpt_prompt = [
        SystemMessage(content="""Você analisa respostas de leads de um serviço de inteligência artificial que cria documentos 
        para advogados. A sua responsabilidade é classificar os leads como Advogado, Nao advogado ou Bot."""),
        HumanMessage(content=content)
    ]

    gpt_answer = chat(gpt_prompt).content

    return gpt_answer