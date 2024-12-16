from fastapi import Depends,HTTPException,status
from services.security import get_current_user


""" 
(
Presidente,
Vice presidente, 
1º secretário, 
2º secretário, 
Tesoureiro, 
Diretor(
    1º Diretor,
    2º Diretor),
Fiscais e Suplentes, Associado
).

"""

def president_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "PRESIDENTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data
        


def socio_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "SOCIO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def vice_president_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "VICE-PRESIDENTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def first_secretary_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "1º SECRETARIO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def second_secretary_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "2º SECRETARIO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data


def treasurer_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "TESOUREIRO":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def first_director_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "1º DIRETOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def second_director_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "2º DIRETOR":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def fiscal_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "FISCAL":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data

def suplente_permission(user_data = Depends(get_current_user)):
    if user_data.cargo != "SUPLENTE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário não autorizado"
        )
    return user_data