import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import pinecone
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
import time
from src.service.embedModel import embed_model
import openai
load_dotenv()

class PineconeClass:
    def __init__(self):
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENVIRONMENT')
        )
        self.index = pinecone.Index(index_name='criabot-response-example-1-free')

    def create_index(self, index_name):
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(
                index_name,
                dimension=1536,
                metric='cosine'
            )

            while not pinecone.describe_index(index_name).status['ready']:
                time.sleep(1)

        return pinecone.Index(index_name)

    def insert_text(self, index, ids, embeds, metadata):
        index.upsert(vectors=[{"id": str(ids), "values": embeds, "metadata": metadata}])

    def get_information_from_vectorstore(self):
        vectorstore = Pinecone(index=pinecone.Index("criabot-response-example-1-free"), embedding=embed_model, text_key="message")
        return vectorstore

    def query_index(self, query_string, filter_results):
        self.set_openai_endpoint()
        embedding = openai.Embedding.create(input=query_string, engine="text-embedding-ada-002")["data"][0]["embedding"]
        query_result = self.index.query([embedding], top_k=2, include_metadata=True, filter=filter_results)
        print(query_result)
        return query_result['matches']

    def set_openai_endpoint(self):
        openai.api_key = os.getenv('API_KEY')
        openai.api_base = os.getenv('BASE_URL')
        openai.api_type = os.getenv('OPENAI_API_TYPE')
        openai.api_version = os.getenv('OPENAI_API_VERSION')