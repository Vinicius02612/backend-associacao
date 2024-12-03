from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from models.models import User

router = APIRouter(prefix="/login")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

def get_email_user(db, emai: str):
    """ Get user by email """
    user = db.query(User).filter(User.email == emai).first()
    return user



async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_email_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario não autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inativo")
    return current_user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_email_user(form_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.email, "token_type": "bearer"}