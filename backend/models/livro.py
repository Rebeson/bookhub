from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .associations import livro_autor, livro_genero


class Livro(Base):
    __tablename__ = "livro"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    titulo: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    subtitulo: Mapped[str | None] = mapped_column(
        String(255)
    )

    isbn: Mapped[str | None] = mapped_column(
        String(20),
        unique=True
    )

    sinopse: Mapped[str | None] = mapped_column(
        Text
    )

    ano_publicacao: Mapped[int | None] = mapped_column(
        SmallInteger
    )

    numero_paginas: Mapped[int | None] = mapped_column(
        Integer
    )

    idioma: Mapped[str | None] = mapped_column(
        String(50)
    )

    capa: Mapped[str | None] = mapped_column(
        String(500)
    )

    editora_id: Mapped[int] = mapped_column(
        ForeignKey("editora.id"),
        nullable=False
    )

    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    editora = relationship(
        "Editora",
        back_populates="livros"
    )

    autores = relationship(
        "Autor",
        secondary=livro_autor,
        back_populates="livros"
    )

    generos = relationship(
        "Genero",
        secondary=livro_genero,
        back_populates="livros"
    )

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="livro"
    )

    resenhas = relationship(
        "Resenha",
        back_populates="livro"
    )

    usuarios = relationship(
        "UsuarioLivro",
        back_populates="livro"
    )