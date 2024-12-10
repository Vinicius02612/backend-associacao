from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from models.models import User
from services.security import verify_password,create_access_token
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from connection.dependences import get_db
from config.config import settings
from jwt import PyJWTError
import jwt
router = APIRouter(prefix="/login")




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

def get_email_user(db, email: str):
    """ Get user by email """
    user = db.query(User).filter(User.email == email).first()
    return user


def authenticate_user(db, email: str, password: str):    
    user = get_email_user(db, email)
    if not user or not verify_password(password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    return user



async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credicais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRETY_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credicais_exception
        token_data = email
    except PyJWTError:
        raise credicais_exception
    
    user = get_email_user(db, token_data)
    if user is None:
        raise credicais_exception
    
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inativo")
    return current_user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user.email)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}