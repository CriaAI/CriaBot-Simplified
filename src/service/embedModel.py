import sys, os
sys.path.insert(0, os.path.abspath(os.curdir))

from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings

load_dotenv()

embed_model = OpenAIEmbeddings(
    deployment="text-embedding-ada-002",
    openai_api_base=os.getenv("BASE_URL"),
    openai_api_key=os.getenv("API_KEY"),
    openai_api_type="azure"
)