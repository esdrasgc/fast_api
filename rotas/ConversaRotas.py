from fastapi import APIRouter, HTTPException

from pydantic import ValidationError

from modelos.Conversa import Conversa, ConversaCreate, ConversaComMensagens
from uuid import uuid4

from fastapi import Depends,Query
from sqlmodel import Session, select
from db import get_session

router = APIRouter(
    prefix='/conversa',
    tags=["Conversa"]
)

@router.post("/", response_model=Conversa)
def create_conversa(*, session: Session = Depends(get_session), conversa: ConversaCreate):
    db_conversa = Conversa.model_validate(conversa, update={"id": uuid4()})
    session.add(db_conversa)
    session.commit()
    session.refresh(db_conversa)
    return db_conversa


@router.get("/", response_model=list[Conversa])
def read_conversa(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    conversa = session.exec(select(Conversa).offset(offset).limit(limit)).all()
    return conversa


@router.get("/{conversa_id}", response_model=ConversaComMensagens)
def read_conversa(*, session: Session = Depends(get_session), conversa_id: int):
    conversa = session.get(Conversa, conversa_id)
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa not found")
    return conversa