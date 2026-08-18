from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .associations import livro_genero


class Genero(Base):
    __tablename__ = "genero"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    descricao: Mapped[str | None] = mapped_column(
        Text
    )

    livros = relationship(
        "Livro",
        secondary=livro_genero,
        back_populates="generos"
    )