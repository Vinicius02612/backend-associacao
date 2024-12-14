from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import  OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from services.security import create_access_token
from sqlalchemy.orm import Session
from connection.dependences import get_db as get_session
from services.security import verify_password
from sqlalchemy import select
from models.models import User
from services.security import (get_current_user)
from schemas.schema import UserToken
import logging


logging.basicConfig(level=logging.DEBUG)

router = APIRouter(prefix="/login")




@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    logging.debug(f"\nDados Recebido de form_data: {form_data.username}\n")
    user = session.scalar(select(User).where(User.email == form_data.username))
    logging.debug(f" \nUser Recebido na rota POST/login/token: {user.name}\n")
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data_payload={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user