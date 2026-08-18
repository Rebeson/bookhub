from datetime import datetime

from pydantic import BaseModel, Field


class LivroBase(BaseModel):
    titulo: str = Field(
        min_length=1,
        max_length=255
    )

    subtitulo: str | None = Field(
        default=None,
        max_length=255
    )

    isbn: str | None = Field(
        default=None,
        max_length=20
    )

    sinopse: str | None = None

    ano_publicacao: int | None = Field(
        default=None,
        gt=0
    )

    numero_paginas: int | None = Field(
        default=None,
        gt=0
    )

    idioma: str | None = Field(
        default=None,
        max_length=50
    )

    capa: str | None = Field(
        default=None,
        max_length=500
    )

    editora_id: int


class LivroCreate(LivroBase):
    pass


class LivroResponse(LivroBase):
    id: int
    data_cadastro: datetime

    class Config:
        from_attributes = True