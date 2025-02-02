
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 

# Cria a engine para PostgreSQL

db = os.environ.get('DATABASE_PUBLIC_URL')

engine = create_engine(f'{db}', echo=True)

# Define a base declarativa
Base = declarative_base()

# Define a classe de modelo
class Receitas(Base):
    __tablename__ = 'Receitas'
    id = Column(Integer, primary_key=True)
    usuario = Column(String)
    nome = Column(String)
    data = Column(String)
    infos = Column(String)
    tipo = Column(String)

class Usuarios(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    senha = Column(Integer)

# Cria o esquema do banco de dados
Base.metadata.create_all(engine)

# Cria uma sessão
Session = sessionmaker(bind=engine)
session = Session()

