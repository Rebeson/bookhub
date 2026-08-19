from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.security import get_current_admin
from backend.database.connection import get_db
from backend.models.editora import Editora
from backend.models.livro import Livro
from backend.schemas.livro import (
    LivroCreate,
    LivroResponse,
    LivroUpdate
)
from backend.models.avaliacao import Avaliacao
from backend.models.resenha import Resenha
from backend.models.usuario_livro import UsuarioLivro
from backend.models.associations import livro_autor, livro_genero


router = APIRouter(
    prefix="/livros",
    tags=["Livros"]
)

@router.post(
    "/",
    response_model=LivroResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_livro(
    dados: LivroCreate,
    usuario_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    editora = db.get(Editora, dados.editora_id)

    if editora is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Editora não encontrada."
        )
    
    if dados.isbn is not None:
        livro_existente = db.scalar(
        select(Livro).where(
            Livro.isbn == dados.isbn
        )
    )

    if livro_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ISBN já cadastrado."
        )

    novo_livro = Livro(
        titulo=dados.titulo,
        subtitulo=dados.subtitulo,
        isbn=dados.isbn,
        sinopse=dados.sinopse,
        ano_publicacao=dados.ano_publicacao,
        numero_paginas=dados.numero_paginas,
        idioma=dados.idioma,
        capa=dados.capa,
        editora_id=dados.editora_id
    )

    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    return novo_livro

@router.get("/", response_model=list[LivroResponse])
def listar_livros(
    db: Session = Depends(get_db)
):
    livros = db.scalars(
        select(Livro)
    ).all()

    return livros


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    return livro

@router.put("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(
    livro_id: int,
    dados: LivroUpdate,
    usuario_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    editora = db.get(Editora, dados.editora_id)

    if editora is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Editora não encontrada."
        )

    if dados.isbn is not None:
        livro_existente = db.scalar(
            select(Livro).where(
                Livro.isbn == dados.isbn,
                Livro.id != livro_id
            )
        )

        if livro_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="ISBN já cadastrado."
            )

    livro.titulo = dados.titulo
    livro.subtitulo = dados.subtitulo
    livro.isbn = dados.isbn
    livro.sinopse = dados.sinopse
    livro.ano_publicacao = dados.ano_publicacao
    livro.numero_paginas = dados.numero_paginas
    livro.idioma = dados.idioma
    livro.capa = dados.capa
    livro.editora_id = dados.editora_id

    db.commit()
    db.refresh(livro)

    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_livro(
    livro_id: int,
    usuario_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    possui_autores = db.scalar(
        select(livro_autor).where(
            livro_autor.c.livro_id == livro_id
        )
    )

    possui_generos = db.scalar(
        select(livro_genero).where(
            livro_genero.c.livro_id == livro_id
        )
    )

    possui_estantes = db.scalar(
        select(UsuarioLivro).where(
            UsuarioLivro.livro_id == livro_id
        )
    )

    possui_avaliacoes = db.scalar(
        select(Avaliacao).where(
            Avaliacao.livro_id == livro_id
        )
    )

    possui_resenhas = db.scalar(
        select(Resenha).where(
            Resenha.livro_id == livro_id
        )
    )

    if any([
        possui_autores,
        possui_generos,
        possui_estantes,
        possui_avaliacoes,
        possui_resenhas
    ]):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir este livro porque ele possui dados relacionados."
        )

    db.delete(livro)
    db.commit()