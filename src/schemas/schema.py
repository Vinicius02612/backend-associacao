from pydantic import BaseModel,field_validator, ConfigDict
from typing import List
from datetime import date, datetime
from validate_docbr import CPF
from email_validator import validate_email, EmailNotValidError
from services.utils import get_password_hash

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
    
    @field_validator("email")
    def email_validate(cls, email):
        try:
            emailInfo = validate_email(email, check_deliverability=False)
            email = emailInfo.normalized
        except EmailNotValidError as e:
            raise ValueError("Email inválido")
        return email
    
    @field_validator("cpf")
    def validete_cpf(cls, _cpf):
        cpf = CPF()
        if not cpf.validate(_cpf):
            raise ValueError("CPF inválido")
        
        new_cpf_mascked = cpf.mask(_cpf)
        return new_cpf_mascked
    
    @field_validator("data_nascimento")
    def validete_data_nascimento(cls, data_nascimento):
        data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
       #usuario deve ser maior de 16 anos
        if data_nascimento.year > 2005:
            raise ValueError("Usuário deve ser maior de 16 anos")

        return data_nascimento
    
    @field_validator("dtassociacao")
    def validete_dtassociacao(cls, dtassociacao):
        #pegar data atual do sistema
        dtassociacao = datetime.now().date()
        return dtassociacao

    model_config = ConfigDict(from_attributes=True)

   

    

    
class UserToken(BaseModel):
    email: str
    cargo:str
    access_token:str
    token_type:str
    exp:int


class SolicitacaoBase(BaseModel):
    id: int
    data: date
    status: str
    iduser: int

    

    model_config = ConfigDict(from_attributes=True)

class SolicitacaoResponse(BaseModel):
    id: int
    data: date
    status: str
    iduser: int

 
    model_config = ConfigDict(from_attributes=True)

class SolicitacaoRequest(BaseModel):
    data: date
    status: str
    iduser: int
    

    model_config = ConfigDict(from_attributes=True)


class MensalidadeBase(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    status: str
    iduser: int

    #definir valores padrão para os campos: valor,status, dtvencimento e dtpagamento, data devencimento deve ser 5 dias uteis após a data de vencimento
    @field_validator("valor")
    def validate_valor(cls, valor):
        if valor < 0:
            raise ValueError("O valor da mensalidade não pode ser negativo")
        new_valor = 5.00

        return new_valor
    
    @field_validator("status")
    def validate_status(cls, status):
        if status not in ["pendente", "pago"]:
            raise ValueError("Status inválido")
        new_status = "pendente"

        return new_status
    
    @field_validator("dtvencimento")
    def validate_dtvencimento(cls, dtvencimento):
        #data de vencimento vai ser no mesmo dia do mes de associação do usuário
        user = UserResponse()
        new_dtvencimento = user.dtassociacao
        dtvencimento = datetime.strptime(new_dtvencimento, "%Y-%m-%d").date()
        return dtvencimento
    
    @field_validator("dtpagamento")
    def validate_dtpagamento(cls, dtpagamento, status):
        #data pagamento é dia que usuário paga a mensalidade
        if status == "pendente":
            dtpagamento = None
        else:
            dtpagamento = datetime.now().date()
        return dtpagamento








    model_config = ConfigDict(from_attributes=True)

class MensalidadeResponse(BaseModel):
    id: int
    valor: float
    dtvencimento: date
    dtpagamento: date
    status: str
    iduser: int
  

    model_config = ConfigDict(from_attributes=True)

class MensalidadeRequest(BaseModel):
    valor: float
    dtvencimento: date
    dtpagamento: date
    status: str
    iduser: int
 

    model_config = ConfigDict(from_attributes=True)

class ProjetosBase(BaseModel):
    id: int
    titulo: str
    dtinicio: date
    dtfim: date
    iduser:int

    model_config = ConfigDict(from_attributes=True)

class ProjetosResponse(BaseModel):
    id: int
    titulo: str
    dtinicio:date
    dtfim: date
    iduser:int

    model_config = ConfigDict(from_attributes=True)

class ProjetosRequest(BaseModel):
    titulo: str
    dtinicio: date
    dtfim: date
    iduser:int
    
    model_config = ConfigDict(from_attributes=True)

class DespesaBase(BaseModel):
    id: int
    valor: float
    data: date
    origem: str

    model_config = ConfigDict(from_attributes=True)

class DespesaResponse(BaseModel):
    id: int
    valor: float
    data: date
    origem: str

    model_config = ConfigDict(from_attributes=True)

class DespesaRequest(BaseModel):
    valor: float
    data: date
    origem: str

    model_config = ConfigDict(from_attributes=True)



class ReceitasResponse(BaseModel):
    id: int
    valor: float
    data: date
    origem: str

    model_config = ConfigDict(from_attributes=True)


class ReceitasRequest(BaseModel):
    valor: float
    data: date
    origem: str

    model_config = ConfigDict(from_attributes=True)

class Relatorio(BaseModel):
    id: int
    despesa: List[DespesaResponse]
    receita: List[ReceitasResponse]

    model_config = ConfigDict(from_attributes=True)


class RelatorioRequest(BaseModel):
    id: int
    despesa: List[DespesaResponse]
    receita: List[ReceitasResponse]

    model_config = ConfigDict(from_attributes=True)