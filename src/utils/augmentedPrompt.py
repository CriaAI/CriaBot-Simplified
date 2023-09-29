import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.service.pineconeClass import PineconeClass

class AugmentedPrompt:
    def stage_1(self, user_last_messages):
        filter_results = {"stage": 1.0}
        vectorstore = PineconeClass().get_information_from_vectorstore()
        results = vectorstore.similarity_search(query=user_last_messages, filter=filter_results, k=3)
        examples = ""

        #I am creating a temporary answer to avoid errors when the vector store is empty
        if len(results) < 3:
            examples = """
                {
                    "Mensagem do lead": "Sim",
                    "Categoria": "Advogado"
                }

                {
                    "Mensagem do lead": "Não",
                    "Categoria": "Nao advogado"
                }

                {
                    "Mensagem do lead": "Olá, tudo bem? Obrigada por entrar em contato conosco. Retornaremos o mais rápido possível.",
                    "Categoria": "Bot"
                }
            """
        else:
            examples = f"""
                {{
                    Mensagem do lead: {results[0].page_content},
                    Categoria": {results[0].metadata["category"]}
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

        augmented_prompt = f"""Baseando-se na resposta do lead, você precisa classificá-lo como Advogado, Não advogado ou Bot.
            Resposta do lead: {user_last_messages}

            Exemplos de resposta que devem ser no formato json:
            {examples}
        """

        return augmented_prompt
    
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