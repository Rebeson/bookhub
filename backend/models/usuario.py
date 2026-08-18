from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    nome_usuario: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    foto_perfil: Mapped[str | None] = mapped_column(
        String(500)
    )

    biografia: Mapped[str | None] = mapped_column(
        Text
    )

    tipo_usuario: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    avaliacoes = relationship(
        "Avaliacao",
        back_populates="usuario"
    )

    resenhas = relationship(
        "Resenha",
        back_populates="usuario"
    )

    livros = relationship(
        "UsuarioLivro",
        back_populates="usuario"
    )