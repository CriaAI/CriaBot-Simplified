import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))
import json
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from src.utils.augmentedPrompt import AugmentedPrompt
from src.config import message_stage_2

load_dotenv()

def openAIstage2(user_last_messages):
    seller_message = "\n".join(message_stage_2)
    formated_message = f'Vendedor: \'\'\'{seller_message}\'\'\'\nLead: \'\'\'{user_last_messages}\'\'\''
    chat = AzureChatOpenAI(
        openai_api_base=os.getenv("BASE_URL"),
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_key=os.getenv("API_KEY"),
        openai_api_type="azure",
        temperature=0.4
    )

    augmented_prompt = AugmentedPrompt()
    gpt_prompt = augmented_prompt.prompt_by_stage(user_last_messages=formated_message, stage=2)
    gpt_answer = chat(gpt_prompt).content
    gpt_answer = gpt_answer.replace("```json", '').replace("```", "")

    try:
        gpt_answer = json.loads(gpt_answer)
        return {"prompt": gpt_prompt, "gpt_answer": gpt_answer}
    except json.JSONDecodeError as e:
        print("A resposta não é um JSON válido:")
