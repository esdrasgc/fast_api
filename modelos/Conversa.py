from enum import Enum
from uuid import UUID
from typing import  Optional
from sqlmodel import SQLModel, Field, Relationship
from modelos.Mensagem import Mensagem

class Conversa(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    id_cookie: Optional[UUID] = Field(default=None)

    class Config:
        orm_mode = True

class ConversaCreate(SQLModel):
    id_cookie: Optional[UUID] | str

class ConversaComMensagens(Conversa):
    mensagens: list[Mensagem] = Relationship(back_populates="conversa")