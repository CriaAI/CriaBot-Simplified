import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

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

    content = f"""Baseando-se na resposta do lead, você precisa sugerir se devemos prosseguir com a conversa ou não.
        Resposta do lead: {user_last_messages}

        Exemplos de resposta no formato json:
        {{
            'Mensagem do lead': 👍,
            'Acao': 'Aceitar'
        }}

        {{
            'Mensagem do lead': 'Sim',
            'Acao': 'Aceitar'
        }}

        {{
            'Mensagem do lead': 'Não',
            'Acao': 'Rejeitar'
        }}
    """

    gpt_prompt = [
        SystemMessage(content="""Você é um vendedor de um serviço de inteligência artificial que cria documentos para advogados. 
        A sua responsabilidade é avaliar se devemos prosseguir com a conversa com o lead e possível cliente dependendo do 
        interesse demonstrado na resposta."""),
        HumanMessage(content=content)
    ]

    gpt_answer = chat(gpt_prompt).content

    return gpt_answer