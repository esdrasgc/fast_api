from fastapi import APIRouter, HTTPException

from pydantic import ValidationError

from modelos.Mensagem import Mensagem, MensagemCreate

from fastapi import Depends,Query
from sqlmodel import Session, select
from db import get_session
from db_faiss import DB_faiss
from uuid import uuid4

router = APIRouter(
    prefix='/mensagem', 
    tags=["Mensagem"]
)

@router.post("/", response_model=Mensagem)
def create_mensagem(*, session: Session = Depends(get_session), mensagem: MensagemCreate):
    db_mensagem = Mensagem.model_validate(mensagem, update={"id": uuid4()})
    session.add(db_mensagem)
    session.commit()
    session.refresh(db_mensagem)
    return db_mensagem


@router.get("/", response_model=list[Mensagem])
def read_mensagemes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    mensagemes = session.exec(select(Mensagem).offset(offset).limit(limit)).all()
    return mensagemes


@router.get("/{mensagem_id}", response_model=Mensagem)
def read_mensagem(*, session: Session = Depends(get_session), mensagem_id: int):
    mensagem = session.get(Mensagem, mensagem_id)
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem not found")
    return mensagem