
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


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