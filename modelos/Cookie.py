from sqlmodel import SQLModel, Field, MetaData
from typing import  Optional
from uuid import UUID, uuid4

class Cookie(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    qtd_acessos: int = 1

    class Config:
        schema = "Cookie" 