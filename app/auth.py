#1. Hash e verificação de senhas com bcrypt
#2. Geração e validação de tokens JWT
#3. Leitura e validadão de cookies para autenticação

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request
from dotenv import load_dotenv
import os       

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


#CryptContext - Configura o bcrypt como o algoritmo de hashing para senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Teste de hash
senha = "1234"
senha_hash = pwd_context.hash(senha)
print(f"Hash: {senha_hash}")

senha_atual = "1234"
verificar_senha = pwd_context.verify(senha_atual, senha_hash)
print(verificar_senha)

# Funçôes de senha
def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)

# Funções de token - JWT
def criar_token(data: dict):
    payload = data.copy()

    # Define o tempo de expiração do token
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})

    # Gera o token JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decodificar_token(token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    