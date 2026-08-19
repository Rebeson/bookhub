from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


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


class LivroCreate(BaseModel):
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

    ano_publicacao: int | None = None

    numero_paginas: int | None = None

    idioma: str | None = Field(
        default=None,
        max_length=50
    )

    capa: str | None = Field(
        default=None,
        max_length=500
    )

    editora_id: int


class LivroUpdate(BaseModel):
    titulo: str
    subtitulo: str | None = None
    isbn: str | None = None
    sinopse: str | None = None
    ano_publicacao: int | None = None
    numero_paginas: int | None = None
    idioma: str | None = None
    capa: str | None = None
    editora_id: int


class LivroResponse(BaseModel):
    id: int
    titulo: str
    subtitulo: str | None = None
    isbn: str | None = None
    sinopse: str | None = None
    ano_publicacao: int | None = None
    numero_paginas: int | None = None
    idioma: str | None = None
    capa: str | None = None
    editora_id: int
    data_cadastro: datetime

    model_config = ConfigDict(from_attributes=True)