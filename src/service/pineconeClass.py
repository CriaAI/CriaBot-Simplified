import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

import pinecone
from langchain.vectorstores import Pinecone
import os
from dotenv import load_dotenv
import time
from src.service.embedModel import embed_model

load_dotenv()

class PineconeClass:
    def __init__(self):
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_ENVIRONMENT')
        )

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
        vectorstore = Pinecone(index=pinecone.Index("cria-ai-bot"), embedding=embed_model.embed_query, text_key="message")
        return vectorstore
