from datetime import datetime, timedelta as datedelta
from jwt import encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from config.config import settings

pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    """criar um novo token JWT que será usado para autenticar o usuário.
    Args:
        data (dict): dados do usuário que será codificado no token.
    Returns:
        str: token JWT.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + datedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRETY_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    """Retorna o hash da senha do usuário.
    Args:
        password (str): senha do usuário.
    Returns:
        str: hash da senha.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Verifica se a senha informada é igual a senha do usuário.
    Args:
        plain_password (str): senha informada pelo usuário.
        hashed_password (str): senha do usuário.
    Returns:
        bool: True se a senha for igual, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)