from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import MensalidadeRequest, MensalidadeResponse
from typing import List
from sqlalchemy.orm import Session
from connection.dependences import get_db
from models.models import Mensalidade, User
from services.security import (get_current_user)

router = APIRouter(prefix="/mensalidades")

@router.get("/", response_model=List[MensalidadeResponse])
def get_mensalidades(db:Session = Depends(get_db),current_user: User = Depends(get_current_user)) -> List[Mensalidade]:
    mensalidades = db.query(Mensalidade).all()
    if not mensalidades:
        raise HTTPException(status_code=404, detail="Não há mensalidades cadastradas")
    return mensalidades


@router.post("/", response_model=MensalidadeResponse, status_code=201)
def post_mensalidades(mensalidade_request: MensalidadeRequest, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)) -> List[Mensalidade]:
    new_mensalidade = Mensalidade(
        **mensalidade_request.model_dump()
    )
    db.add(new_mensalidade)
    db.commit()
    db.refresh(new_mensalidade)

    return new_mensalidade
