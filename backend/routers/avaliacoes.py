from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.avaliacao import Avaliacao
from backend.models.livro import Livro
from backend.schemas.avaliacao import AvaliacaoCreate, AvaliacaoResponse, AvaliacaoUpdate
from backend.core.security import get_current_user


router = APIRouter(
    prefix="/avaliacoes",
    tags=["Avaliações"]
)


@router.post(
    "/",
    response_model=AvaliacaoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_avaliacao(
    dados: AvaliacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    livro = db.get(Livro, dados.livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    avaliacao_existente = (
        db.query(Avaliacao)
        .filter(
            Avaliacao.usuario_id == usuario_atual.id,
            Avaliacao.livro_id == dados.livro_id
        )
        .first()
    )

    if avaliacao_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já avaliou este livro."
        )

    agora = datetime.now()

    nova_avaliacao = Avaliacao(
        usuario_id=usuario_atual.id,
        livro_id=dados.livro_id,
        nota=dados.nota,
        data_avaliacao=agora,
        data_atualizacao=agora
    )

    db.add(nova_avaliacao)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já avaliou este livro."
        )

    db.refresh(nova_avaliacao)

    return nova_avaliacao


@router.get(
    "/livro/{livro_id}",
    response_model=list[AvaliacaoResponse]
)
def listar_avaliacoes_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    avaliacoes = (
        db.query(Avaliacao)
        .filter(Avaliacao.livro_id == livro_id)
        .order_by(Avaliacao.data_avaliacao.desc())
        .all()
    )

    return avaliacoes


@router.get(
    "/{avaliacao_id}",
    response_model=AvaliacaoResponse
)
def consultar_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db)
):
    avaliacao = db.get(Avaliacao, avaliacao_id)

    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada."
        )

    return avaliacao


@router.put(
    "/{avaliacao_id}",
    response_model=AvaliacaoResponse
)
def atualizar_avaliacao(
    avaliacao_id: int,
    dados: AvaliacaoUpdate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    avaliacao = db.get(Avaliacao, avaliacao_id)

    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada."
        )

    if avaliacao.usuario_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode alterar esta avaliação."
        )

    avaliacao.nota = dados.nota
    avaliacao.data_atualizacao = datetime.now()

    db.commit()
    db.refresh(avaliacao)

    return avaliacao


@router.delete(
    "/{avaliacao_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_avaliacao(
    avaliacao_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    avaliacao = db.get(Avaliacao, avaliacao_id)

    if not avaliacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avaliação não encontrada."
        )

    if avaliacao.usuario_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode excluir esta avaliação."
        )

    db.delete(avaliacao)
    db.commit()

    return None