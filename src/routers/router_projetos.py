from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import ProjetosResponse, ProjetosRequest
from typing import List
from sqlalchemy.orm import Session
from connection.dependences import get_db
from models.models import Projetos


router = APIRouter(prefix="/projetos")

#retorna todos os projetos em forma de lista
@router.get("/", response_model=List[ProjetosResponse],status_code=200)
def get_projetos(db:Session = Depends(get_db)) -> ProjetosResponse:
    projetos = db.query(Projetos).all()
    if not projetos:
        raise HTTPException(status_code=404, detail="Não há projetos cadastrados")
    else:
        return projetos


@router.post("/", response_model=ProjetosResponse, status_code=201)
def post_projetos(projetos: ProjetosRequest, db: Session = Depends(get_db)) -> Projetos:
    new_projetos = Projetos(
        **projetos.model_dump()
    )
    db.add(new_projetos)
    db.commit()
    db.refresh(new_projetos)

    return new_projetos

@router.put("/{id}", response_model=ProjetosResponse)
def projetos_update(id:int, projetos: ProjetosRequest, db: Session = Depends(get_db)) -> Projetos:
    projetos = db.query(Projetos).filter(Projetos.id == id).first()
    if not projetos:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    for key, value in projetos.dict().items():
        setattr(projetos, key, value)
   
    db.commit()
    db.refresh(projetos)
    return projetos


@router.delete("/{id}", status_code=204)
def projetos_delete(id:int, db: Session = Depends(get_db)):
    projetos = db.query(Projetos).filter(Projetos.id == id).first()
    db.delete(projetos)
    db.commit()
    return None

@router.get("/{titulo}", response_model=ProjetosResponse)
def get_projetos_by_titulo(titulo:str, db:Session = Depends(get_db)) -> ProjetosResponse:
    projetos = db.query(Projetos).filter(Projetos.titulo == titulo).first()
    return projetos