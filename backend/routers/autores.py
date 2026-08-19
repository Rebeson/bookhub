from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.autor import Autor
from backend.schemas.autor import AutorCreate, AutorResponse, AutorUpdate
from backend.core.security import get_current_admin


router = APIRouter(
    prefix="/autores",
    tags=["Autores"]
)


@router.post(
    "/",
    response_model=AutorResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_autor(
    dados: AutorCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    autor_existente = db.scalar(
        select(Autor).where(
            Autor.nome == dados.nome
        )
    )

    if autor_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um autor com este nome."
        )

    autor = Autor(
        nome=dados.nome,
        biografia=dados.biografia,
        data_nascimento=dados.data_nascimento,
        foto=dados.foto
    )

    db.add(autor)
    db.commit()
    db.refresh(autor)

    return autor


@router.get(
    "/",
    response_model=list[AutorResponse]
)
def listar_autores(
    db: Session = Depends(get_db)
):
    autores = db.scalars(
        select(Autor).order_by(Autor.nome)
    ).all()

    return autores


@router.get(
    "/{autor_id}",
    response_model=AutorResponse
)
def buscar_autor(
    autor_id: int,
    db: Session = Depends(get_db)
):
    autor = db.get(Autor, autor_id)

    if autor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado."
        )

    return autor


@router.put(
    "/{autor_id}",
    response_model=AutorResponse
)
def atualizar_autor(
    autor_id: int,
    dados: AutorUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    autor = db.get(Autor, autor_id)

    if autor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Autor não encontrado."
        )

    if dados.nome is not None:
        autor_existente = db.scalar(
            select(Autor).where(
                Autor.nome == dados.nome,
                Autor.id != autor_id
            )
        )

        if autor_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe outro autor com este nome."
            )

        autor.nome = dados.nome

    if dados.biografia is not None:
        autor.biografia = dados.biografia

    if dados.data_nascimento is not None:
        autor.data_nascimento = dados.data_nascimento

    if dados.foto is not None:
        autor.foto = dados.foto

    db.commit()
    db.refresh(autor)

    return autor