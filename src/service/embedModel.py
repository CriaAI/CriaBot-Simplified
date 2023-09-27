import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

#embed_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))

embed_model = OpenAIEmbeddings(
    #deployment="cria-ai-chatbot",
    model="text-embedding-ada-002",
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_type="azure"
)