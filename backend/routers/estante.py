from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, date

from backend.database.connection import get_db
from backend.models.usuario import Usuario
from backend.models.livro import Livro
from backend.models.usuario_livro import UsuarioLivro
from backend.core.security import get_current_user
from backend.schemas.estante import EstanteAtualizacao

router = APIRouter(
    prefix="/estante",
    tags=["Estante"]
)


@router.get("/minha-estante")
def minha_estante(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    estante = (
        db.query(UsuarioLivro)
        .join(Livro, UsuarioLivro.livro_id == Livro.id)
        .filter(UsuarioLivro.usuario_id == usuario_atual.id)
        .all()
    )

    return [
        {
            "livro_id": item.livro_id,
            "titulo": item.livro.titulo,
            "status_leitura": item.status_leitura,
            "pagina_atual": item.pagina_atual,
            "data_adicao": item.data_adicao
        }
        for item in estante
    ]


@router.post("/{livro_id}", status_code=status.HTTP_201_CREATED)
def adicionar_livro_estante(
    livro_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    livro_estante = (
        db.query(UsuarioLivro)
        .filter(
            UsuarioLivro.usuario_id == usuario_atual.id,
            UsuarioLivro.livro_id == livro_id
        )
        .first()
    )

    if livro_estante:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este livro já está na sua estante."
        )

    novo_livro = UsuarioLivro(
        usuario_id=usuario_atual.id,
        livro_id=livro_id,
        status_leitura="QUERO_LER",
        pagina_atual=0,
        data_adicao=datetime.now()
    )

    db.add(novo_livro)
    db.commit()

    return {
        "message": "Livro adicionado à estante com sucesso."
    }


@router.put("/{livro_id}")
def atualizar_estante(
    livro_id: int,
    dados: EstanteAtualizacao,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    item_estante = (
        db.query(UsuarioLivro)
        .filter(
            UsuarioLivro.usuario_id == usuario_atual.id,
            UsuarioLivro.livro_id == livro_id
        )
        .first()
    )

    if not item_estante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado na sua estante."
        )

    if dados.pagina_atual > item_estante.livro.numero_paginas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A página atual não pode ser maior que o número de páginas do livro."
        )

    if (
    dados.status_leitura.value == "LIDO"
    and dados.pagina_atual < item_estante.livro.numero_paginas
):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Para marcar o livro como LIDO, é necessário chegar à última página."
    )

    status_anterior = item_estante.status_leitura
    novo_status = dados.status_leitura.value

    item_estante.status_leitura = novo_status
    item_estante.pagina_atual = dados.pagina_atual

    if novo_status == "LENDO" and status_anterior != "LENDO":
        if item_estante.data_inicio is None:
            item_estante.data_inicio = date.today()

    if novo_status == "LIDO" and status_anterior != "LIDO":
        if item_estante.data_conclusao is None:
            item_estante.data_conclusao = date.today()

    if novo_status == "QUERO_LER":
        item_estante.data_inicio = None
        item_estante.data_conclusao = None

    if novo_status == "LENDO":
        item_estante.data_conclusao = None

    db.commit()
    db.refresh(item_estante)

    return {
        "message": "Estante atualizada com sucesso.",
        "livro_id": item_estante.livro_id,
        "status_leitura": item_estante.status_leitura,
        "pagina_atual": item_estante.pagina_atual
    }


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_da_estante(
    livro_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    item_estante = (
        db.query(UsuarioLivro)
        .filter(
            UsuarioLivro.usuario_id == usuario_atual.id,
            UsuarioLivro.livro_id == livro_id
        )
        .first()
    )

    if not item_estante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado na sua estante."
        )

    db.delete(item_estante)
    db.commit()

    return None


@router.get("/{livro_id}")
def consultar_livro_estante(
    livro_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
):
    item_estante = (
        db.query(UsuarioLivro)
        .filter(
            UsuarioLivro.usuario_id == usuario_atual.id,
            UsuarioLivro.livro_id == livro_id
        )
        .first()
    )

    if not item_estante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado na sua estante."
        )

    return {
        "livro_id": item_estante.livro_id,
        "titulo": item_estante.livro.titulo,
        "status_leitura": item_estante.status_leitura,
        "pagina_atual": item_estante.pagina_atual,
        "total_paginas": item_estante.livro.numero_paginas,
        "data_adicao": item_estante.data_adicao,
        "data_inicio": item_estante.data_inicio,
        "data_conclusao": item_estante.data_conclusao
    }