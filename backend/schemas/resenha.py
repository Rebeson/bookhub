from datetime import datetime

from pydantic import BaseModel, Field


class ResenhaCreate(BaseModel):
    livro_id: int
    titulo: str = Field(
        min_length=1,
        max_length=200
    )
    conteudo: str = Field(
        min_length=1
    )


class ResenhaUpdate(BaseModel):
    titulo: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )
    conteudo: str | None = Field(
        default=None,
        min_length=1
    )


class ResenhaResponse(BaseModel):
    id: int
    usuario_id: int
    livro_id: int
    titulo: str
    conteudo: str
    data_publicacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True