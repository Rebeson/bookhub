from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.favorito import Favorito
from backend.models.livro import Livro
from backend.core.security import get_current_user
from backend.schemas.favorito import FavoritoResponse


router = APIRouter(
    prefix="/favoritos",
    tags=["Favoritos"]
)


@router.get(
    "",
    response_model=list[FavoritoResponse]
)
def listar_favoritos(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    favoritos = (
        db.query(Favorito)
        .filter(
            Favorito.usuario_id == usuario_atual.id
        )
        .all()
    )

    return favoritos


@router.post(
    "/{livro_id}",
    response_model=FavoritoResponse,
    status_code=status.HTTP_201_CREATED
)
def adicionar_favorito(
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

    favorito_existente = (
        db.query(Favorito)
        .filter(
            Favorito.usuario_id == usuario_atual.id,
            Favorito.livro_id == livro_id
        )
        .first()
    )

    if favorito_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este livro já está nos seus favoritos."
        )

    novo_favorito = Favorito(
        usuario_id=usuario_atual.id,
        livro_id=livro_id,
        data_adicao=datetime.now()
    )

    db.add(novo_favorito)
    db.commit()
    db.refresh(novo_favorito)

    return novo_favorito


@router.get(
    "/{livro_id}",
    response_model=FavoritoResponse
)
def consultar_favorito(
    livro_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    favorito = (
        db.query(Favorito)
        .filter(
            Favorito.usuario_id == usuario_atual.id,
            Favorito.livro_id == livro_id
        )
        .first()
    )

    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Este livro não está nos seus favoritos."
        )

    return favorito


@router.delete(
    "/{livro_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remover_favorito(
    livro_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    favorito = (
        db.query(Favorito)
        .filter(
            Favorito.usuario_id == usuario_atual.id,
            Favorito.livro_id == livro_id
        )
        .first()
    )

    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Este livro não está nos seus favoritos."
        )

    db.delete(favorito)
    db.commit()

    return None