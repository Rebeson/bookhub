from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from backend.core.security import get_current_admin
from backend.database.connection import get_db
from backend.schemas.livro import (
    LivroCreate,
    LivroResponse,
    LivroUpdate,
    LivroListaResponse
)
from backend.models.editora import Editora
from backend.models.livro import Livro
from backend.models.autor import Autor
from backend.models.avaliacao import Avaliacao
from backend.models.resenha import Resenha
from backend.models.usuario_livro import UsuarioLivro
from backend.models.genero import Genero
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


@router.get("/{livro_id}/autores")
def listar_autores_do_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    return livro.autores


@router.post("/{livro_id}/autores/{autor_id}", status_code=status.HTTP_201_CREATED)
def adicionar_autor_ao_livro(
    livro_id: int,
    autor_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    autor = db.get(Autor, autor_id)

    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado."
        )

    if autor in livro.autores:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este autor já está associado ao livro."
        )

    livro.autores.append(autor)

    db.commit()

    return {
        "message": "Autor associado ao livro com sucesso."
    }


@router.delete("/{livro_id}/autores/{autor_id}")
def remover_autor_do_livro(
    livro_id: int,
    autor_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    autor = db.get(Autor, autor_id)

    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado."
        )

    if autor not in livro.autores:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Este autor não está associado ao livro."
        )

    livro.autores.remove(autor)

    db.commit()

    return {
        "message": "Autor removido do livro com sucesso."
    }


@router.get("/{livro_id}/generos")
def listar_generos_do_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    return livro.generos


@router.post(
    "/{livro_id}/generos/{genero_id}",
    status_code=status.HTTP_201_CREATED
)
def adicionar_genero_ao_livro(
    livro_id: int,
    genero_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    genero = db.get(Genero, genero_id)

    if not genero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gênero não encontrado."
        )

    if genero in livro.generos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este gênero já está associado ao livro."
        )

    livro.generos.append(genero)

    db.commit()

    return {
        "message": "Gênero associado ao livro com sucesso."
    }


@router.delete("/{livro_id}/generos/{genero_id}")
def remover_genero_do_livro(
    livro_id: int,
    genero_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    genero = db.get(Genero, genero_id)

    if not genero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gênero não encontrado."
        )

    if genero not in livro.generos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Este gênero não está associado ao livro."
        )

    livro.generos.remove(genero)

    db.commit()

    return {
        "message": "Gênero removido do livro com sucesso."
    }



@router.get("/", response_model=list[LivroListaResponse])
def listar_livros(
    db: Session = Depends(get_db)
):

    resultados = (
        db.query(
            Livro,
            func.avg(Avaliacao.nota).label("media"),
            func.count(Avaliacao.id).label("quantidade")
        )
        .outerjoin(
            Avaliacao,
            Livro.id == Avaliacao.livro_id
        )
        .group_by(Livro.id)
        .all()
    )

    return [
        {
            "id": livro.id,
            "titulo": livro.titulo,
            "ano_publicacao": livro.ano_publicacao,
            "idioma": livro.idioma,
            "numero_paginas": livro.numero_paginas,
            "capa": livro.capa,
            "editora": livro.editora.nome if livro.editora else None,

            "autores": [
                {
                    "id": autor.id,
                    "nome": autor.nome
                }
                for autor in livro.autores
            ],

            "generos": [
                {
                    "id": genero.id,
                    "nome": genero.nome
                }
                for genero in livro.generos
            ],

            "media_avaliacoes": (
                round(float(media), 2)
                if media is not None
                else None
            ),

            "quantidade_avaliacoes": quantidade
        }

        for livro, media, quantidade in resultados
    ]

