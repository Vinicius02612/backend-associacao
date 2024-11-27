from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import UserResponse, UserRequest
from typing import List
from sqlalchemy.orm import Session
from connection.dependences import get_db
from models.models import User 
#importar Dependes para usar o banco de dados



router = APIRouter(prefix="/users")

#retorna todos os associados em forma de lista


@router.get("/", response_model=List[UserResponse])
def get_user_associates(db:Session = Depends(get_db)) -> List[UserResponse]:
    user = db.query(User).all()
    if not user:
        raise HTTPException(status_code=404, detail="Não há usuários cadastrados")
    else:
        return user

@router.get("/{id}", response_model=UserResponse)
def get_user_associate(id:int, db:Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.id == id).first()
    return user

#rota para buscar usuarui pelo cpf
@router.get("/cpf/{cpf}", response_model=UserResponse)
def get_user_by_cpf(cpf:str, db:Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.cpf == cpf).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user_associate(user_request: UserRequest, db: Session = Depends(get_db)) -> User:
    #verificar se o cpf já existe
    user = db.query(User).filter(User.cpf == user_request.cpf).first()
    if user:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    else:
        new_user = User(
            **user_request.model_dump()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    return new_user

@router.put("/{id}", response_model=UserResponse)
def update_user(id:int, user_request: UserRequest, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    for key, value in user_request.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{id}", status_code=204)
def delete_user(id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    else:
        db.delete(user)
        db.commit()
    return None

#rota para buscar um usuario pelo nome ou cpf
@router.get("/{name_or_cpf}", response_model=UserResponse)
def get_user_by_name_or_cpf(name_or_cpf:str, db:Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.name == name_or_cpf or User.cpf == name_or_cpf).first()
    print(user)
    return user
