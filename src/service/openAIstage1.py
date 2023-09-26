import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

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

    content = f"""Baseando-se na resposta do lead, você precisa sugerir se devemos prosseguir com a conversa ou não.
        Resposta do lead: {user_last_messages}

        Exemplos de resposta que devem ser extritamente no formato json abaixo:
        {{
            Mensagem do lead: Olá, não prestamos serviços jurídicos.,
            Acao: Rejeitar,
            Motivo: Não é advogado
        }}

        {{
            Mensagem do lead: Sim,
            Acao: Aceitar,
            Motivo: É advogado
        }}

        {{
            Mensagem do lead: Sim, prestamos serviços jurídicos,
            Acao: Aceitar,
            Motivo: É advogado
        }}

        {{
            Mensagem do lead: Olá, tudo bem? Como podemos ajudar? Em breve entraremos em contato com você.,
            Acao: Rejeitar,
            Motivo: É um bot
        }}
    """

    gpt_prompt = [
        SystemMessage(content="""Você analisa respostas de leads de um serviço de inteligência artificial que cria documentos 
        para advogados. A sua responsabilidade é avaliar se devemos prosseguir com a conversa com o lead e possível cliente 
        dependendo do interesse demonstrado na resposta e classificá-lo como advogado, não advogado ou bot. Responda no formato 
        json"""),
        HumanMessage(content=content)
    ]

    gpt_answer = chat(gpt_prompt).content

    return gpt_answer