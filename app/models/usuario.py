from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    #tipo de usuario, pode ser "admin" ou "user", por padrão é "user"
    role = Column(String(30), nullable=False, default="user")
    ativo = Column(Boolean, default=True)

    criado_em = Column(DateTime, server_default=func.now())
    