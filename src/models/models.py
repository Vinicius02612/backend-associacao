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
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    cpf = Column(String, index=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    senha = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    cargo = Column(String, nullable=False)
    dtassociacao = Column(Date, nullable=False)
    _mensalidades = relationship("Mensalidade", backref="User", cascade="all, delete-orphan")
    _projetos = relationship("Projetos", backref="User", cascade="all, delete-orphan")
    _solicitacoes = relationship("Solicitacao", backref="User", cascade="all, delete-orphan")
    created_at = Column(DateTime(timezone=True), server_default=func.now(),nullable=True)
    updated_at = Column( DateTime(timezone=True), onupdate=func.now(), nullable=True)

class Solicitacao(Base):
    __tablename__ = 'solicitacoes'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    data = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    iduser = Column(Integer, ForeignKey('user.id'), nullable=False)
    _user = relationship("User", backref="solicitacoes")



class Mensalidade(Base):
    __tablename__ = 'mensalidades'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    valor = Column(Float, nullable=False, default=5.00)
    dtvencimento = Column(Date, nullable=False)
    dtpagamento = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    iduser = Column(Integer, ForeignKey('user.id'), nullable=False)
    # Relacionamento com User
    _socio = relationship("User", backref="mensalidades")


class Projetos(Base):
    __tablename__ = 'projetos'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    titulo = Column(String, nullable=False)
    dtinicio = Column(Date, nullable=False)
    dtfim = Column(Date, nullable=False)
    # Relacionamento com User
    iduser = Column(Integer, ForeignKey('user.id'), nullable=False)
    _socios = relationship("User", secondary="user_projetos", backref="projetos")
    
class Despesas(Base):
    __tablename__ = 'despesas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float)
    data = Column(Date, nullable=False)
    origem = Column(String, nullable=False)



class Receitas(Base):
    __tablename__ = 'receitas'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    valor = Column(Float)
    data = Column(Date, nullable=False)
    origem = Column(String, nullable=False)
   


class Relatorio(Base):
    __tablename__ = 'relatorios'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    data = Column(Date, nullable=False, server_default=func.now())
    idDespesa = Column(Integer, ForeignKey('despesas.id'))
    idReceita = Column(Integer, ForeignKey('receitas.id'))
    _despesa = relationship("Despesas", backref="relatorios")
    _receita = relationship("Receitas", backref="relatorios")

