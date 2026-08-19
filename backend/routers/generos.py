from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.genero import Genero
from backend.schemas.generos import GeneroCreate, GeneroResponse, GeneroUpdate
from backend.core.security import get_current_admin


router = APIRouter(
    prefix="/generos",
    tags=["Gêneros"]
)


@router.get("/", response_model=list[GeneroResponse])
def listar_generos(
    db: Session = Depends(get_db)
):
    generos = db.scalars(
        select(Genero).order_by(Genero.nome)
    ).all()

    return generos


@router.post(
    "/",
    response_model=GeneroResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_genero(
    genero: GeneroCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    genero_existente = db.scalar(
        select(Genero).where(
            Genero.nome == genero.nome
        )
    )

    if genero_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um gênero com este nome."
        )

    novo_genero = Genero(
        nome=genero.nome,
        descricao=genero.descricao
    )

    db.add(novo_genero)
    db.commit()
    db.refresh(novo_genero)

    return novo_genero


@router.get("/{genero_id}", response_model=GeneroResponse)
def buscar_genero(
    genero_id: int,
    db: Session = Depends(get_db)
):
    genero = db.get(Genero, genero_id)

    if not genero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gênero não encontrado."
        )

    return genero


@router.put("/{genero_id}", response_model=GeneroResponse)
def atualizar_genero(
    genero_id: int,
    dados: GeneroUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    genero = db.get(Genero, genero_id)

    if not genero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gênero não encontrado."
        )

    if dados.nome is not None:
        genero_existente = db.scalar(
            select(Genero).where(
                Genero.nome == dados.nome,
                Genero.id != genero_id
            )
        )

        if genero_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro gênero com este nome."
            )

        genero.nome = dados.nome

    if dados.descricao is not None:
        genero.descricao = dados.descricao

    db.commit()
    db.refresh(genero)

    return genero


@router.delete(
    "/{genero_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_genero(
    genero_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    genero = db.get(Genero, genero_id)

    if not genero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gênero não encontrado."
        )

    if genero.livros:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir um gênero associado a livros."
        )

    db.delete(genero)
    db.commit()