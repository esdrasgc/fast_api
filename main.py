import pathlib
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI

from typing import Union
from fastapi import FastAPI, status, Response

from uuid import uuid4, UUID
import uvicorn
from sqlmodel import Session, SQLModel, create_engine, select
from db import create_db_and_tables

from rotas import ConversaRotas, MensagemRotas
from db_faiss import DB_faiss

# Carregar variáveis de ambiente do arquivo .env
env_path = pathlib.Path.cwd() / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Clara API", description="API para o projeto Clara", version="0.1.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(ConversaRotas.router)
app.include_router(MensagemRotas.router)

class InputSchema(BaseModel):
    query: str

@app.get('/')
async def home():
    return {'hello': 'world'}

@app.post('/search')
async def search(input: InputSchema):
    query = input.query
    db_faiss = DB_faiss().db_faiss
    results = db_faiss.similarity_search(query, 5)
    return {'text': [x.page_content for x in results]}