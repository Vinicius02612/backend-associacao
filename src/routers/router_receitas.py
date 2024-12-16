from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import ReceitasRequest, ReceitasResponse
from typing import List
from sqlalchemy.orm import Session
from connection.dependences import get_db
from models.models import Receitas,User
from services.permissions import (president_permission)


router = APIRouter(prefix="/receitas")

import logging

logging.basicConfig(level=logging.DEBUG)

@router.get("/", response_model=List[ReceitasResponse])
def get_receitas(db:Session = Depends(get_db), current_user: User = Depends(president_permission)) -> List[Receitas]:
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
  
    receitas = db.query(Receitas).all()
    if not receitas:
        raise HTTPException(status_code=404, detail="Não há receitas cadastradas")
    return receitas


@router.post("/", response_model=ReceitasResponse, status_code=201)
def post_receitas(receita_request: ReceitasRequest, db: Session = Depends(get_db), current_user: User = Depends(president_permission)) -> List[Receitas]:
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuario não permitido")
    new_receita = Receitas(
        **receita_request.model_dump()
    )
    db.add(new_receita)
    db.commit()
    db.refresh(new_receita)

    return new_receita

@router.put("/{id}", response_model=ReceitasResponse)
def receitas_update(id:int, receita_request: ReceitasRequest, db: Session = Depends(get_db), current_user: User = Depends(president_permission)) -> Receitas:
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
      
    receita = db.query(Receitas).filter(Receitas.id == id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    for key, value in receita_request.model_dump().items():
        setattr(receita, key, value)
    
    db.commit()
    db.refresh(receita)
    return receita

@router.delete("/{id}", response_model=ReceitasResponse)
def receitas_delete(id:int, db: Session = Depends(get_db),current_user: User = Depends(president_permission)) -> Receitas:
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    receita = db.query(Receitas).filter(Receitas.id == id).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    db.delete(receita)
    db.commit()
    return receita

