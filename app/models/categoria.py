# Tabela Categoria


from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
    ativa = Column(Boolean, default=True)

    # Relacionamento com Produto
    # O parâmetro lazy="select" garante que os produtos relacionados sejam carregados apenas quando acessados, evitando consultas desnecessárias.
    produtos = relationship("Produto", back_populates="categoria", lazy="select")