from enum import Enum
from uuid import UUID
from typing import  Optional
from sqlmodel import SQLModel, Field, Relationship

class Mensagem(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    id_conversa: UUID = Field(default=None, foreign_key="conversa.id")
    texto: str
    resposta_gpt: Optional[str] = Field(default=None)

    class Config:
        orm_mode = True

class MensagemCreate(SQLModel):
    id_conversa: UUID
    texto: str
