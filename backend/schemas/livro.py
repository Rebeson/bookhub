from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


# =====================================================
# LIVRO BASE
# =====================================================

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


# =====================================================
# CRIAÇÃO DE LIVRO
# =====================================================

class LivroCreate(LivroBase):

    pass


# =====================================================
# ATUALIZAÇÃO DE LIVRO
# =====================================================

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


# =====================================================
# RESPOSTA COMPLETA DO LIVRO
# =====================================================

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

    model_config = ConfigDict(
        from_attributes=True
    )


# =====================================================
# AUTOR NA LISTAGEM DE LIVROS
# =====================================================

class AutorLivroResponse(BaseModel):

    id: int

    nome: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =====================================================
# GÊNERO NA LISTAGEM DE LIVROS
# =====================================================

class GeneroLivroResponse(BaseModel):

    id: int

    nome: str

    model_config = ConfigDict(
        from_attributes=True
    )


# =====================================================
# RESPOSTA DA LISTAGEM DE LIVROS
# =====================================================

class LivroListaResponse(BaseModel):

    id: int

    titulo: str

    ano_publicacao: int | None

    idioma: str | None

    numero_paginas: int | None

    editora: str | None

    autores: list[AutorLivroResponse]

    generos: list[GeneroLivroResponse]

    media_avaliacoes: float | None

    quantidade_avaliacoes: int

    model_config = ConfigDict(
        from_attributes=True
    )

