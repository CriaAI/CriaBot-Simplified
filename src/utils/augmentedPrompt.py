import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from src.service.pineconeClass import PineconeClass

class AugmentedPrompt:
    def stage_1(self, user_last_messages):
        filter = {"stage": 1.0}
        vectorstore = PineconeClass().get_information_from_vectorstore()
        results = vectorstore.similarity_search(query=user_last_messages, filter=filter, k=3)
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

        augmented_prompt = f"""Baseando-se na resposta do lead, você precisa classificá-lo como advogado, não advogado ou bot.
            Resposta do lead: {user_last_messages}

            Exemplos de resposta que devem ser extritamente no formato json abaixo:
            {examples}
        """

        return augmented_prompt
    
    def stage_2(self, user_last_messages):
        filter = {"stage": 2.0}
        vectorstore = PineconeClass().get_information_from_vectorstore()
        results = vectorstore.similarity_search(query=user_last_messages, filter=filter, k=3)
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

        augmented_prompt = f"""Baseando-se na resposta do lead, você precisa classificá-lo como interessado ou não interessado.
            Resposta do lead: {user_last_messages}

            Exemplos de resposta que devem ser extritamente no formato json abaixo:
            {examples}
        """

        return augmented_prompt