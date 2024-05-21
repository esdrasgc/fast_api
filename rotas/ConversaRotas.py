from fastapi import APIRouter, HTTPException

from pydantic import ValidationError

from modelos.Conversa import Conversa, ConversaCreate, ConversaComMensagens
from modelos.Cookie import Cookie
from uuid import uuid4, UUID

from fastapi import Depends,Query
from sqlmodel import Session, select
from db import get_session

router = APIRouter(
    prefix='/conversa',
    tags=["Conversa"]
)

@router.post("/", response_model=Conversa)
def create_conversa(*, session: Session = Depends(get_session), conversa: ConversaCreate):
    id_cookie = conversa.id_cookie
    if isinstance(id_cookie, str):
        try:
            id_cookie = UUID(id_cookie)
        except:
            pass
    if isinstance(id_cookie, UUID):
        cookie = session.get(Cookie, id_cookie)
    else:
        cookie = None
    if not cookie:
        # create a new cookie
        cookie = Cookie(id = uuid4())
    else:
        cookie.qtd_acessos += 1
    session.add(cookie)
    session.commit()
    session.refresh(cookie)

    db_conversa = Conversa.model_validate(conversa, update={"id": uuid4(), 'id_cookie': cookie.id})
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
def read_conversa(*, session: Session = Depends(get_session), conversa_id: UUID):
    conversa = session.get(Conversa, conversa_id)
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa not found")
    return conversa