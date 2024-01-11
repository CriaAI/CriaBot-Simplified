import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.service.pineconeClass import PineconeClass
from langchain.schema import SystemMessage, HumanMessage, AIMessage
class AugmentedPrompt:
    def __init__(self):
        self.gpt_prompt = [SystemMessage(content="""Meta Contexto\n## Você é um auxiliar agente classificador.\n- Você receberá a mensagem de um vendedor e a resposta de um cliente;\n- Seu papel é classificar a resposta do cliente, retornando o número da ação a ser tomada.\n## Sobre a estrutura de resposta:\n- Você deve sempre responder na estrutura de JSON válido!""")]

    def prompt_by_stage(self, user_last_messages:list[dict], stage:int):
        filter_results = {"stage": stage}
        pinecone = PineconeClass()
        query_results = pinecone.query_index(user_last_messages, filter_results=filter_results)
        for result in query_results:
            metadata = result['metadata']
            self.gpt_prompt.append(HumanMessage(content=f"""Retorne a ação para a seguinte conversa: \'\'\'{metadata["messages"]}\'\'\'"""))
            self.gpt_prompt.append(AIMessage(content=metadata['response']))
        self.gpt_prompt.append(HumanMessage(content=f"""Retorne a ação para a seguinte conversa: \'\'\'{user_last_messages}\'\'\'"""))

        return self.gpt_prompt
    def stage_1(self, user_last_messages):
        #\n## Das respostas possíveis\n- Retorne {\"action\":0} se o cliente NÃO presta serviços jurídicos;\n- Retorne {\"action\":1} se o cliente presta serviços jurídicos;\n- Retorne {\"action\":2} se não estiver claro quanto se o cliente presta serviços jurídicos ou não;
        filter_results = {"stage": 1.0}
        pinecone = PineconeClass()
        query_results = pinecone.query_index(user_last_messages, filter_results=filter_results)
        for result in query_results:
            metadata = result['metadata']
            self.gpt_prompt.append(HumanMessage(content=f"""Retorne a ação para a seguinte conversa: \'\'\'{metadata["messages"]}\'\'\'"""))
            self.gpt_prompt.append(AIMessage(content=metadata['response']))
        self.gpt_prompt.append(HumanMessage(content=f"""Retorne a ação para a seguinte conversa: \'\'\'{user_last_messages}\'\'\'"""))

        return self.gpt_prompt

    def stage_2(self, user_last_messages):
        filter_results = {"stage": 2.0}
        vectorstore = PineconeClass().get_information_from_vectorstore()
        results = vectorstore.similarity_search(query=user_last_messages, filter=filter_results, k=3)
        examples = ""

        #I am creating a temporary answer to avoid errors when the vector store is empty
        if len(results) < 3:
            examples = """
                {
                    "Mensagem do lead": "Sim",
                    "Categoria": "Interessado"
                }

                {
                    "Mensagem do lead": "Não",
                    "Categoria": "Nao interessado"
                }

                {
                    "Mensagem do lead": "👍",
                    "Categoria": "Interessado"
                }
            """
        else:
            examples = f"""
                {{
                    Mensagem do lead: {results[0].page_content},
                    Categoria: {results[0].metadata["category"]}
                }}

                {{
                    Mensagem do lead: {results[1].page_content},
                    Categoria: {results[1].metadata["category"]}
                }}

                {{
                    Mensagem do lead: {results[2].page_content},
                    Categoria: {results[2].metadata["category"]}
                }}
            """

        augmented_prompt = f"""Baseando-se na resposta do lead, você precisa classificá-lo como Interessado ou Não interessado.
            Resposta do lead: {user_last_messages}

            Exemplos de resposta que devem ser no formato json:
            {examples}
        """

        return augmented_prompt

    def stage_4(self, user_last_messages):
        filter_results = {"stage": 4.0}
        vectorstore = PineconeClass().get_information_from_vectorstore()
        results = vectorstore.similarity_search(query=user_last_messages, filter=filter_results, k=3)
        examples = ""

        #I am creating a temporary answer to avoid errors when the vector store is empty
        if len(results) < 3:
            examples = """
                {
                    "Pergunta do lead": "Olá, e quais são os benefícios desse serviço de vocês?",
                    "Resposta": "Com a Cria.AI você economiza tempo criando documentos e assim sobra mais tempo para atender ainda mais clientes."
                }

                {
                    "Pergunta do lead": "Mas como eu irei conseguir personalizar os documentos para cada cliente?",
                    "Resposta": "Na nossa plataforma, você pode inserir todos os dados relevantes para cada documento que precisares gerar."
                }
            """
        else:
            examples = f"""
                {{
                    "Pergunta do lead": "{results[0].page_content}",
                    "Resposta": "{results[0].metadata["gpt_answer"]}"
                }}

                {{
                    "Pergunta do lead": "{results[1].page_content}",
                    "Resposta": "{results[1].metadata["gpt_answer"]}"
                }}

                {{
                    "Pergunta do lead": "{results[2].page_content}",
                    "Resposta": "{results[2].metadata["gpt_answer"]}"
                }}
            """

        augmented_prompt = f"""Baseando-se na pergunta do lead, você deve responde-lo com o objetivo de sanar as suas dúvidas.
            Pergunta do lead: {user_last_messages}

            Exemplos de resposta que devem ser no formato json:
            {examples}
        """

        return augmented_prompt