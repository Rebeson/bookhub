from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.security import (
    get_current_user,
    hash_password
)
from backend.database.connection import get_db
from backend.models.usuario import Usuario
from backend.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.scalar(
        select(Usuario).where(
            (Usuario.email == usuario.email) |
            (Usuario.nome_usuario == usuario.nome_usuario)
        )
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail ou nome de usuário já cadastrado."
        )

    novo_usuario = Usuario(
        nome=usuario.nome,
        nome_usuario=usuario.nome_usuario,
        email=usuario.email,
        senha_hash=hash_password(usuario.senha),
        foto_perfil=usuario.foto_perfil,
        biografia=usuario.biografia,
        tipo_usuario="USUARIO",
        ativo=True
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.get(
    "/me",
    response_model=UsuarioResponse
)
def obter_usuario_atual(
    usuario: Usuario = Depends(get_current_user)
):
    return usuario


@router.put(
    "/me",
    response_model=UsuarioResponse
)
def atualizar_usuario_atual(
    dados: UsuarioUpdate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if dados.email is not None:
        usuario_existente = db.scalar(
            select(Usuario).where(
                Usuario.email == dados.email,
                Usuario.id != usuario.id
            )
        )

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado."
            )

        usuario.email = dados.email

    if dados.nome_usuario is not None:
        usuario_existente = db.scalar(
            select(Usuario).where(
                Usuario.nome_usuario == dados.nome_usuario,
                Usuario.id != usuario.id
            )
        )

        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nome de usuário já cadastrado."
            )

        usuario.nome_usuario = dados.nome_usuario

    if dados.nome is not None:
        usuario.nome = dados.nome

    if dados.foto_perfil is not None:
        usuario.foto_perfil = dados.foto_perfil

    if dados.biografia is not None:
        usuario.biografia = dados.biografia

    db.commit()
    db.refresh(usuario)

    return usuario