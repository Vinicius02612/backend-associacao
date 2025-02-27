from datetime import datetime, timedelta as datedelta
from jwt import encode
from jose import JWTError
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from config.config import settings
from connection.dependences import get_db  as get_session
from fastapi import Depends,HTTPException, status
from http import HTTPStatus
from jwt import encode, decode, DecodeError
from fastapi.security import OAuth2PasswordBearer
from schemas.schema import UserToken as TokenData
from models.models import User
from sqlalchemy import select
from services.utils import verify_password
from http import HTTPStatus

import logging

logging.basicConfig(level=logging.DEBUG)

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

def create_access_token(data_payload: dict):
    """criar um novo token JWT que será usado para autenticar o usuário.
    Args:
        data (dict): dados do usuário que será codificado no token.
    Returns:
        str: token JWT.
    """
    to_encode = data_payload.copy()

    #tempo de expiração do token
    expire = datetime.now(tz=ZoneInfo('UTC')) + datedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    #adiciona a data de expiração ao token
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRETY_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt



def verify_token(token: str):
    """Verifica se o token é válido.
    Args:
        token (str): token JWT.
    Returns:
        TokenData: dados do token.
    """
    try:
        payload = decode(token, settings.SECRETY_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get('sub')

        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return token_data


def authenticate_user( db:Session,  email: str, password: str):
    """Autentica o usuário.
    Args:
        email (str): email do usuário.
        password (str): senha do usuário.
        session (Session): sessão do banco de dados.
    Returns:
        User: usuário autenticado.
    
    """
    user_email = db.query(User).filter(User.email == email).first()
    
    if not user_email or not verify_password(password, user_email.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return user_email




def get_current_user( session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, settings.SECRETY_KEY, algorithms=[settings.ALGORITHM])
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user