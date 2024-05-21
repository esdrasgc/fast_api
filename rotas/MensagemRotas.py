from fastapi import APIRouter, HTTPException

from pydantic import ValidationError

from modelos.Mensagem import Mensagem, MensagemCreate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from fastapi import Depends,Query
from sqlmodel import Session, select
from db import get_session
from db_faiss import DB_faiss
from uuid import uuid4
import requests
from uuid import UUID
from typing import List

router = APIRouter(
    prefix='/mensagem', 
    tags=["Mensagem"]
)

msg_inicial = """
Voce é uma inteligencia artificial criada para ajudar mulheres que estão passando por conflitos familiares. Voce deve ser acolhedor para que elas se sintam bem e a vontade para conversar com voce.

Se for preciso redirecionar para um advogado, indique que o usuario envie uma mensagem pelo whatsapp para o seguinte numero: (11) 91909-1967

Abaixo estão algumas informações curadas por uma advogada especialista para ajudar a responder. Evite respostas vagas. Se for necessário mais informações para responder, peça para a usuária fornecer mais detalhes e considere todas as interações como um dialogo.
""" 
msg_final = """
Caso alguma pergunta fuja do conhecimento acima, voce deve responder: Sua pergunta foi selecionada para ser respondida em breve pelos nossos advogados parceiros. Para uma resposta ágil, mande uma mensagem no whatsapp para o número (11) 98848-9812 e um de nossos advogados irá te responder o mais rápido possível.
"""

def generate_gpt_response(texto:str, historico:List[Mensagem], k:int):
    db_faiss = DB_faiss().db_faiss
    results = db_faiss.similarity_search(texto, k)
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DB_faiss().api_key}"
    }
    bot_context = "\n\n".join([x.page_content for x in results])
    bot_context = msg_inicial + bot_context + msg_final

    historico_txt = []
    for h in historico:
        historico_txt.append({"role": "user", "content": h.texto if h.texto else ""})
        historico_txt.append({"role": "assistant", "content": h.resposta_gpt if h.resposta_gpt else ""})

    messages = [{"role": "system", "content": bot_context}] + historico_txt + [{"role": "user", "content": texto}]
    print("vV"*100)
    print(messages)
    print("vV"*100)

    data = {
        "model": "gpt-4o",
        "messages": messages
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise HTTPException(status_code=500, detail="Erro ao gerar resposta GPT")
    # return {"content": bot_context}


@router.post("/", response_model=Mensagem)
def create_mensagem(*, session: Session = Depends(get_session), mensagem: MensagemCreate, k:int=6):
    texto = mensagem.texto
    historico = session.exec(select(Mensagem).where(Mensagem.id_conversa == mensagem.id_conversa).order_by(Mensagem.criada.desc()).limit(5)).all()
    resposta_gpt = generate_gpt_response(texto, historico, k)
    db_mensagem = Mensagem.model_validate(mensagem, update={"id": uuid4(), 'resposta_gpt': resposta_gpt})
    session.add(db_mensagem)
    session.commit()
    session.refresh(db_mensagem)
    return db_mensagem


@router.get("/", response_model=list[Mensagem])
def read_mensagens(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    id_conversa: UUID = None
):
    if id_conversa:
        mensagens = session.exec(select(Mensagem).where(Mensagem.id_conversa == id_conversa).offset(offset).limit(limit)).all()
    else:
        mensagens = session.exec(select(Mensagem).offset(offset).limit(limit)).all()
    return mensagens


@router.get("/{mensagem_id}", response_model=Mensagem)
def read_mensagem(*, session: Session = Depends(get_session), mensagem_id: UUID):
    mensagem = session.get(Mensagem, mensagem_id)
    if not mensagem:
        raise HTTPException(status_code=404, detail="Mensagem not found")
    return mensagem