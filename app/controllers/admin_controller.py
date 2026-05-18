from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.auth import get_admin, hash_senha

#APIROUTER - Agrupa as rotas de autenticação do arquivo com o prefixo "/auth"
router = APIRouter(prefix="/usuarios", tags=["Usuários"])

#Configuta para renderizar os templates HTML
templates = Jinja2Templates(directory="app/templates")


#Lista de usuários - Somente para administradores
@router.get("/")
def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    admin = Depends(get_admin),  # Bloqueia o acesso para usuários não administradores
):
    # Pegar todos os usuários do banco de dados
    usuarios = db.query(Usuario).order_by(Usuario.nome).all()
    return templates.TemplateResponse(
        request,
        "usuarios/index.html",
        {"request": request,
         "admin": admin,
         "usuarios": usuarios
         }
    )