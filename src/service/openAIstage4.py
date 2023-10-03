import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import json
import time
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.utils.augmentedPrompt import AugmentedPrompt

load_dotenv()

def openAIstage4(user_last_messages):
    chat = AzureChatOpenAI(
        openai_api_base=os.getenv("BASE_URL"),
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_key=os.getenv("API_KEY"),
        openai_api_type="azure",
        temperature=0.4
    )

    augmented_prompt = AugmentedPrompt()
    content = augmented_prompt.stage_4(user_last_messages)
 
    gpt_prompt = [
        SystemMessage(content="""Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados.
        A empresa que você trabalha se chama Cria.AI e você deve responder as perguntas do lead da melhor forma possível."""),
        HumanMessage(content=content)
    ]

    gpt_answer = chat(gpt_prompt).content

    try:
        gpt_answer = json.loads(gpt_answer)["Resposta"]
        return {"prompt": content, "gpt_answer": gpt_answer}
    except json.JSONDecodeError as e:
        print("A resposta não é um JSON válido:")
        return {"prompt": content, "gpt_answer": gpt_answer}
    