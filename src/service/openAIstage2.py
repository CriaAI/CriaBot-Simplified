import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.utils.augmentedPrompt import AugmentedPrompt

load_dotenv()

def openAIstage2(user_last_messages):
    chat = AzureChatOpenAI(
        openai_api_base=os.getenv("BASE_URL"),
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_key=os.getenv("API_KEY"),
        openai_api_type="azure",
        temperature=0.4
    )

    augmented_prompt = AugmentedPrompt()
    content = augmented_prompt.stage_2(user_last_messages)

    gpt_prompt = [
        SystemMessage(content="""Você analisa conversas com possíveis clientes de um serviço de inteligência artificial que 
        cria documentos para advogados. A sua responsabilidade é classificar o lead como Interessado ou Nao interessado."""),
        HumanMessage(content=content)
    ]

    gpt_answer = chat(gpt_prompt).content
    
    return {"prompt": content, "gpt_answer": gpt_answer}