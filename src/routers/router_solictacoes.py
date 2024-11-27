from fastapi import APIRouter,Depends,HTTPException
from schemas.schema import SolicitacaoResponse, SolicitacaoRequest
from typing import List
from sqlalchemy.orm import Session
from connection.dependences import get_db
from models.models import Solicitacao


router = APIRouter(prefix="/solicitacoes")

#retorna todas as solicitações em forma de lista
@router.get("/", response_model=List[SolicitacaoResponse])
def get_solicitacoes(db:Session = Depends(get_db)) -> List[Solicitacao]:
    solicitacoes = db.query(Solicitacao).all()
    return solicitacoes

@router.post("/", response_model=SolicitacaoResponse, status_code=201)
def post_solicitacoes(solicitacao: SolicitacaoRequest, db: Session = Depends(get_db)) -> Solicitacao:
    new_solicitacao = Solicitacao(
        **solicitacao.model_dump()
    )
    db.add(new_solicitacao)
    db.commit()
    db.refresh(new_solicitacao)

    return Solicitacao(**new_solicitacao.model_dump())


@router.put("/{id}", response_model=SolicitacaoResponse)
def solicitation_update(id:int, solicitacao: SolicitacaoRequest, db: Session = Depends(get_db)) -> Solicitacao:
    solicitacao = db.query(Solicitacao).filter(Solicitacao.id == id).first()
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    for key, value in solicitacao.dict().items():
        setattr(solicitacao, key, value)
   
    db.commit()
    db.refresh(solicitacao)
    return solicitacao

@router.delete("/{id}", status_code=204)
def solicitation_delete(id:int, db: Session = Depends(get_db)):
    solicitacao = db.query(Solicitacao).filter(Solicitacao.id == id).first()
    db.delete(solicitacao)
    db.commit()
    return None