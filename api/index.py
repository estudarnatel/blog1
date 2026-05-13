
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    Form
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List
from models import Aprovado, Blog
# import database

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from pathlib import Path

from mangum import Mangum

# ======================================================
# APP
# ======================================================


BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()

# ======================================================
# SESSION MIDDLEWARE
# ======================================================

app.add_middleware(
    SessionMiddleware,
    secret_key="minha_chave_super_secreta"
)

# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# STATIC FILES
# ======================================================

# app.mount("/CSS", StaticFiles(directory="CSS"), name="css")
# app.mount("/JS", StaticFiles(directory="JS"), name="js")



# ======================================================
# TEMPLATES
# ======================================================

# templates = Jinja2Templates(directory=".")


app.mount(
    "/CSS",
    StaticFiles(directory=str(BASE_DIR / "CSS")),
    name="css"
)

app.mount(
    "/JS",
    StaticFiles(directory=str(BASE_DIR / "JS")),
    name="js"
)


templates = Jinja2Templates(
    directory=str(BASE_DIR)
)

# ======================================================
# LOGIN FIXO
# ======================================================

USERNAME = "admin"
PASSWORD = "admin"

# ======================================================
# PÁGINA INICIAL
# ======================================================

@app.get("/api/", response_class=HTMLResponse)
def home(request: Request):

    # ==========================================
    # CONTADOR DE VISITAS
    # ==========================================

    visitas = request.cookies.get("visitas")

    if visitas is None:
        visitas = 1
    else:
        visitas = int(visitas) + 1

    # ==========================================
    # COOKIE DO NOME
    # ==========================================

    nome = request.cookies.get("nome")

    if nome:
        saudacao = f"Olá, {nome}!"
    else:
        saudacao = "Olá, visitante!"

    # ==========================================
    # LOGIN
    # ==========================================

    usuario_logado = request.session.get("user")

    # ==========================================
    # RESPONSE
    # ==========================================

    response = templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "visitas": visitas,
            "saudacao": saudacao,
            "usuario_logado": usuario_logado
        }
    )

    # salva cookie
    response.set_cookie(
        key="visitas",
        value=str(visitas)
    )

    return response

# ======================================================
# SALVAR NOME NO COOKIE
# ======================================================

@app.get("/api/nome/{nome}")
def salvar_nome(nome: str):

    response = RedirectResponse(
        url="/",
        status_code=302
    )

    response.set_cookie(
        key="nome",
        value=nome
    )

    return response

# ======================================================
# LOGIN - FORMULÁRIO
# ======================================================

@app.get("/api/login", response_class=HTMLResponse)
def login_form(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "mostrar_login": True,
            "erro": None
        }
    )

# ======================================================
# LOGIN - PROCESSA
# ======================================================

@app.post("/api/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    # if username == USERNAME and password == PASSWORD:
    if password == PASSWORD:

        # request.session["user"] = username

        # return RedirectResponse(
        #     url="/perfil",
        #     status_code=302
        # )
        # salva sessão
        request.session["user"] = username

        # redireciona
        response = RedirectResponse(
            url="/api/perfil",
            status_code=302
        )

        # atualiza cookie do nome
        response.set_cookie(
            key="nome",
            value=username
        )

        return response

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "mostrar_login": True,
            "erro": "Usuário ou senha inválidos."
        }
    )

# ======================================================
# PERFIL (PROTEGIDA)
# ======================================================

@app.get("/api/perfil", response_class=HTMLResponse)
def perfil(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse(
            url="/api/login",
            status_code=302
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "perfil": True,
            "usuario": user
        }
    )

# ======================================================
# LOGOUT
# ======================================================

# @app.get("/logout")
# def logout(request: Request):

#     request.session.clear()

#     return RedirectResponse(
#         url="/login",
#         status_code=302
#     )

# ======================================================
# LOGOUT
# ======================================================

@app.get("/api/logout")
def logout(request: Request):

    # limpa sessão
    request.session.clear()

    # redireciona
    response = RedirectResponse(
        url="/api/login",
        status_code=302
    )

    # remove cookie do nome
    response.delete_cookie("nome")

    return response


# ======================================================
# MANGUM
# ======================================================

handler = Mangum(app)
