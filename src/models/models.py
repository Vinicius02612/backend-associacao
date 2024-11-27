from sqlalchemy import Column, Date,DateTime, ForeignKey, Integer, String, Float, Table

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from connection.database import Base


# Tabela de associação para User e Projetos
user_projetos = Table(
    'user_projetos',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('projeto_id', Integer, ForeignKey('projetos.id'))
)
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    cpf = Column(String, index=True)
    data_nascimento = Column(Date)
    senha = Column(String)
    quantidade = Column(Integer)
    cargo = Column(String)
    dtassociacao = Column(Date)
    _mensalidades = relationship("Mensalidade", backref="User", cascade="all, delete-orphan")
    _projetos = relationship("Projetos", backref="User", cascade="all, delete-orphan")
    _solicitacoes = relationship("Solicitacao", backref="User", cascade="all, delete-orphan")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Solicitacao(Base):
    __tablename__ = 'solicitacoes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date)
    status = Column(String)
    iduser = Column(Integer, ForeignKey('user.id'))
    _user = relationship("User", backref="solicitacoes")



class Mensalidade(Base):
    __tablename__ = 'mensalidades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float)
    dtvencimento = Column(Date)
    dtpagamento = Column(Date)
    iduser = Column(Integer, ForeignKey('user.id'))
    # Relacionamento com User
    _socio = relationship("User", backref="mensalidades")


class Projetos(Base):
    __tablename__ = 'projetos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    dtinicio = Column(Date)
    dtfim = Column(Date)
    # Relacionamento com User
    iduser = Column(Integer, ForeignKey('user.id'))
    _socios = relationship("User", secondary="user_projetos", backref="projetos")
    
class Despesas(Base):
    __tablename__ = 'despesas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float)
    data = Column(Date)
    origem = Column(String)



class Receitas(Base):
    __tablename__ = 'receitas'
    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    data = Column(Date)
    origem = Column(String)
   


class Relatorio(Base):
    __tablename__ = 'relatorios'
    id = Column(Integer, primary_key=True)
    data = Column(Date)
    idDespesa = Column(Integer, ForeignKey('despesas.id'))
    idReceita = Column(Integer, ForeignKey('receitas.id'))
    _despesa = relationship("Despesas", backref="relatorios")
    _receita = relationship("Receitas", backref="relatorios")

