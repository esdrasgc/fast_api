from enum import Enum
from uuid import UUID
from typing import  Optional
from sqlmodel import SQLModel, Field, Relationship, String
import datetime

class Mensagem(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    id_conversa: UUID = Field(default=None, foreign_key="conversa.id")
    texto: str = Field(sa_type=String(2500))
    resposta_gpt: Optional[str] = Field(default=None, sa_type=String(8000))
    criada: Optional[datetime.datetime] = Field(
        default_factory=datetime.datetime.now,
    )

    class Config:
        orm_mode = True

class MensagemCreate(SQLModel):
    id_conversa: UUID
    texto: str
