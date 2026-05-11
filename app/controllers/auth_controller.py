from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import hash_senha, verificar_senha, criar_token

#APIROUTER - Agrupa as rotas de autenticação do arquivo com o prefixo "/auth"
router = APIRouter(prefix="/auth", tags=["Autenticação"])

#Configuta para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")

# Rota para a tela de cadastro
@router.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/cadastro.html",
        {"request": request}
    )

# Rota para a tela de login
@router.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "auth/login.html",
        {"request": request}
    )

# Rota para criar um usuario no banco de dados
@router.post("/cadastro")
def fazer_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    # Verificar se o usuário já existe
    usuario_existente = db.query(Usuario).filter_by(email=email).first()
    if usuario_existente:
        return templates.TemplateResponse(
            request,
            "auth/cadastro.html",
            {"request": request, "erro": "Este email já está cadastrado."}
        )

    # Criar o novo usuário
    nova_senha = hash_senha(senha)
    novo_usuario = Usuario(nome=nome, email=email, senha_hash=nova_senha)
    db.add(novo_usuario)
    db.commit()

    # Redirecionar para a tela de login
    return RedirectResponse(url="/auth/login?cadastro=successo", status_code=status.HTTP_302_FOUND)
