from typing import Union
import json
import pathlib
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Carregar variáveis de ambiente do arquivo .env
env_path = pathlib.Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)
# Usar a chave de API carregada do arquivo .env
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key não encontrada. Certifique-se de que o arquivo .env está configurado corretamente.")

embeddings = OpenAIEmbeddings(openai_api_key=api_key, model="text-embedding-3-large")

db = FAISS.load_local("db_faiss", embeddings, allow_dangerous_deserialization=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)


class InputSchema(BaseModel):
    query: str

@app.get('/')
async def home():
    return {'hello': 'world'}

@app.post('/search')
async def search(input: InputSchema):
    query = input.query
    results = db.similarity_search(query, 5)
    return {'text': [x.page_content for x in results]}