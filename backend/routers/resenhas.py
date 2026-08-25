from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.livro import Livro
from backend.models.resenha import Resenha
from backend.core.security import get_current_user
from backend.schemas.resenha import ResenhaCreate, ResenhaResponse, ResenhaUpdate


router = APIRouter(
    prefix="/resenhas",
    tags=["Resenhas"]
)


@router.post(
    "",
    response_model=ResenhaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_resenha(
    dados: ResenhaCreate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    livro = db.get(Livro, dados.livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    resenha_existente = (
        db.query(Resenha)
        .filter(
            Resenha.usuario_id == usuario_atual.id,
            Resenha.livro_id == dados.livro_id
        )
        .first()
    )

    if resenha_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Você já possui uma resenha para este livro."
        )

    agora = datetime.now()

    nova_resenha = Resenha(
        usuario_id=usuario_atual.id,
        livro_id=dados.livro_id,
        titulo=dados.titulo,
        conteudo=dados.conteudo,
        data_publicacao=agora,
        data_atualizacao=agora
    )

    db.add(nova_resenha)
    db.commit()
    db.refresh(nova_resenha)

    return nova_resenha


@router.get(
    "/livro/{livro_id}",
    response_model=list[ResenhaResponse]
)
def listar_resenhas_livro(
    livro_id: int,
    db: Session = Depends(get_db)
):
    livro = db.get(Livro, livro_id)

    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro não encontrado."
        )

    resenhas = (
        db.query(Resenha)
        .filter(
            Resenha.livro_id == livro_id
        )
        .order_by(
            Resenha.data_publicacao.desc()
        )
        .all()
    )

    return resenhas


@router.get(
    "/{resenha_id}",
    response_model=ResenhaResponse
)
def consultar_resenha(
    resenha_id: int,
    db: Session = Depends(get_db)
):
    resenha = db.get(Resenha, resenha_id)

    if not resenha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resenha não encontrada."
        )

    return resenha


@router.put(
    "/{resenha_id}",
    response_model=ResenhaResponse
)
def atualizar_resenha(
    resenha_id: int,
    dados: ResenhaUpdate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    resenha = db.get(Resenha, resenha_id)

    if not resenha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resenha não encontrada."
        )

    if resenha.usuario_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para alterar esta resenha."
        )

    if dados.titulo is not None:
        resenha.titulo = dados.titulo

    if dados.conteudo is not None:
        resenha.conteudo = dados.conteudo

    resenha.data_atualizacao = datetime.now()

    db.commit()
    db.refresh(resenha)

    return resenha


@router.delete(
    "/{resenha_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remover_resenha(
    resenha_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user)
):
    resenha = db.get(Resenha, resenha_id)

    if not resenha:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resenha não encontrada."
        )

    if resenha.usuario_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para excluir esta resenha."
        )

    db.delete(resenha)
    db.commit()

    return None