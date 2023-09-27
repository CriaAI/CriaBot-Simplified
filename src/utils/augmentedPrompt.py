import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import pinecone
from src.service.pineconeClass import PineconeClass

class AugmentedPrompt:
    def stage_1(self, user_last_messages, embed_model):
        vectorstore = PineconeClass().get_information_from_vectorstore(pinecone.Index("cria-ai-stage1"), embed_model)
        results = vectorstore.similarity_search(user_last_messages, k=3)

        #I am creating a temporary array to avoid errors
        if len(results) < 3:
            results = [
                {
                    "page_content": "Sim",
                    "metadata": {
                        "category": "lawyer"
                    }
                },
                {
                    "page_content": "No",
                    "metadata": {
                        "category": "not_lawyer"
                    }
                },
                {
                    "page_content": "Olá, tudo bem? Obrigada por entrar em contato conosco. Retornaremos o mais rápido possível.",
                    "metadata": {
                        "category": "bot"
                    }
                }
            ]

        augmented_prompt = f"""Baseando-se na resposta do lead, você precisa classificá-lo como advogado, não advogado ou bot.
            Resposta do lead: {user_last_messages}

            Exemplos de resposta que devem ser extritamente no formato json abaixo:
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

        return augmented_prompt