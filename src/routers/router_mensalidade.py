from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import MensalidadeRequest, MensalidadeResponse
from typing import List
from sqlalchemy.orm import Session
from connection.dependences import get_db
from models.models import Mensalidade, User
from services.permissions import (president_permission, socio_permission)

router = APIRouter(prefix="/mensalidades")

@router.get("/", response_model=List[MensalidadeResponse])
def get_mensalidades(db:Session = Depends(get_db),permissions_president: User = Depends(president_permission)) -> List[Mensalidade]:
    if  permissions_president.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    mensalidades = db.query(Mensalidade).all()
    if not mensalidades:
        raise HTTPException(status_code=404, detail="Não há mensalidades cadastradas")
    return mensalidades


@router.post("/", response_model=MensalidadeResponse, status_code=201)
def post_mensalidades(mensalidade_request: MensalidadeRequest, db: Session = Depends(get_db),permissions: User = Depends(president_permission)) -> List[Mensalidade]:
    if permissions.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    new_mensalidade = Mensalidade(
        **mensalidade_request.model_dump()
    )
    db.add(new_mensalidade)
    db.commit()
    db.refresh(new_mensalidade)

    return new_mensalidade

