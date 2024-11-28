from pydantic import BaseModel,field_validator
from typing import List
from datetime import date, datetime
from validate_docbr import CPF
from services.security import get_password_hash

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    cpf: str
    data_nascimento: date
    senha: str
    quantidade: int
    cargo: str
    dtassociacao: date

    class Config:
        orm_mode = True

class UserRequest(BaseModel):
    name: str
    email: str
    cpf: str
    data_nascimento: str
    senha: str
    quantidade: int
    cargo: str
    dtassociacao: date

    @field_validator("senha")
    def senha_validate(cls, senha):
        if len(senha) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres")
        hashed_password = get_password_hash(senha)

        return hashed_password
    class Config:
        orm_mode = True

    

    
class UserToken(BaseModel):
    access_token:str
    user: str
    exp:str
class SolicitacaoBase(BaseModel):
    id: int
    data: date
    status: str
    iduser: int



    class Config:
        orm_mode = True

class SolicitacaoResponse(BaseModel):
    id: int
    data: date
    status: str
    iduser: int

 

    class Config:
        orm_mode = True

class SolicitacaoRequest(BaseModel):
    data: date
    status: str
    iduser: int
    

    class Config:
        orm_mode = True


class MensalidadeBase(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    iduser: int


    class Config:
        orm_mode = True

class MensalidadeResponse(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    iduser: int
  

    class Config:
        orm_mode = True

class MensalidadeRequest(BaseModel):
    valor: float
    dtvencimento: date
    dtpagamento: date
    iduser: int
 

    class Config:
        orm_mode = True

class ProjetosBase(BaseModel):
    id: int
    titulo: str
    dtinicio: date
    dtfim: date
    iduser:int

    class Config:
        orm_mode = True

class ProjetosResponse(BaseModel):
    id: int
    titulo: str
    dtinicio:date
    dtfim: date
    iduser:int

    class Config:
        orm_mode = True

class ProjetosRequest(BaseModel):
    titulo: str
    dtinicio: date
    dtfim: date
    iduser:int
    class Config:
        orm_mode = True

class DespesaBase(BaseModel):
    id: int
    valor: float
    data: date
    origem: str

    class Config:
        orm_mode = True

class DespesaResponse(BaseModel):
    id: int
    valor: float
    data: date
    origem: str

    class Config:
        orm_mode = True

class DespesaRequest(BaseModel):
    valor: float
    data: date
    origem: str

    class Config:
        orm_mode = True



class ReceitasResponse(BaseModel):
    id: int
    valor: float
    data: date
    origem: str

    class Config:
        orm_mode = True


class ReceitasRequest(BaseModel):
    valor: float
    data: date
    origem: str

    class Config:
        orm_mode = True

class Relatorio(BaseModel):
    id: int
    despesa: List[DespesaResponse]
    receita: List[ReceitasResponse]

    class Config:
        orm_mode = True


class RelatorioRequest(BaseModel):
    id: int
    despesa: List[DespesaResponse]
    receita: List[ReceitasResponse]

    class Config:
        orm_mode = True