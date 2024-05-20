import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class DB_faiss:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("API key não encontrada. Certifique-se de que o arquivo .env está configurado corretamente.")
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key, model="text-embedding-3-large")
        self.db_faiss = FAISS.load_local("db_faiss", self.embeddings, allow_dangerous_deserialization=True)