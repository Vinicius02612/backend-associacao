from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import UserResponse, UserRequest
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from connection.dependences import get_db  as get_session
from models.models import User 
from services.security import (get_current_user)
from services.permissions import president_permission
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
#importar Dependes para usar o banco de dados

import logging
logging.basicConfig(level=logging.DEBUG)

router = APIRouter(prefix="/users")

#retorna todos os associados em forma de lista


@router.get("/", response_model=List[UserResponse])
def get_user_associates( db:Session = Depends(get_session)) -> List[UserResponse]:

    user = db.query(User).all()
    if not user:
        raise HTTPException(status_code=404, detail="Não há usuários cadastrados")
    else:
        return user

@router.get("/{id}", response_model=UserResponse)
def get_user_associate(id:int, db:Session = Depends(get_session), current_user:User = Depends(president_permission)) -> UserResponse:
    
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    
    
    user = db.query(User).filter(User.id == id).first()
    return user

#rota para buscar usuarui pelo cpf
@router.get("/{cpf}", response_model=UserResponse)
def get_user_by_cpf(cpf:str, db:Session = Depends(get_session),current_user: User = Depends(president_permission)) -> UserResponse:
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    else:
        user = db.query(User).filter(User.cpf == cpf).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user_associate(user_request: UserRequest, session: Session = Depends(get_session)) -> User:

    logging.debug(f"Recebido: {user_request}\n")

    
    db_user = session.scalar(
        select(User).where(
            (User.cpf == user_request.cpf) | (User.email == user_request.email)
        )
    )
    if db_user:
        if db_user.cpf == user_request.cpf:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="CPF já cadastrado")
        elif db_user.email == user_request.email:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Email já cadastrado")
    
    new_user = User(
        **user_request.model_dump()
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user



@router.put("/{id}", response_model=UserResponse)
def update_user(id:int, user_request: UserRequest, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)) -> User:
    if current_user.id != id:
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    
    try:
        user = session.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        for key, value in user_request.model_dump().items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
    
        return user
    
    except IntegrityError:
        session.rollback()
        
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, 
            detail="CPF ou email já cadastrado"
        )


@router.delete("/{id}", status_code=204)
def delete_user(id:int, session: Session = Depends(get_session),  current_user: User = Depends(president_permission)):
    if current_user.cargo != "PRESIDENTE":
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    else:
        user = session.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        else:
            session.delete(user)
            session.commit()
        return None

#rota para buscar um usuario pelo nome ou cpf
@router.get("/{name_or_cpf}", response_model=UserResponse)
def get_user_by_name_or_cpf(name_or_cpf:str, db:Session = Depends(get_session),  current_user: User = Depends(get_current_user)) -> UserResponse:
    if current_user.id != id:
        raise HTTPException(status_code=403, detail="Usuário não autorizado")
    else:
        user = db.query(User).filter(User.name == name_or_cpf or User.cpf == name_or_cpf).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user
