from pydantic import BaseModel,field_validator
from typing import List
from datetime import date, datetime

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


    @field_validator("cpf", mode="before")
    def cpf_validator(cls, value):
        if len(value) != 11:
            raise ValueError("CPF deve conter 11 digitos")
        return value
    
  


class SolicitacaoBase(BaseModel):
    id: int
    data: str
    status: str
    idusuario: int
    usuario: UserResponse


    class Config:
        orm_mode = True

class SolicitacaoResponse(BaseModel):
    id: int
    data: date
    status: str
    idusuario: int
    usuario: UserResponse
 

    class Config:
        orm_mode = True

class SolicitacaoRequest(BaseModel):
    data: str
    status: str
    idusuario: int
    usuario: UserRequest


    class Config:
        orm_mode = True


class MensalidadeBase(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    idSocio: int
    socio: UserResponse

    class Config:
        orm_mode = True

class MensalidadeResponse(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    idSocio: int
    socio: UserResponse

    class Config:
        orm_mode = True

class MensalidadeRequest(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    idSocio: int
    socio: UserResponse

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



class Receitas(BaseModel):
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
    receita: List[Receitas]

    class Config:
        orm_mode = True


class RelatorioRequest(BaseModel):
    id: int
    despesa: List[DespesaResponse]
    receita: List[Receitas]

    class Config:
        orm_mode = True