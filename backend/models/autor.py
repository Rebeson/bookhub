from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .associations import livro_autor


class Autor(Base):
    __tablename__ = "autor"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    biografia: Mapped[str | None] = mapped_column(
        Text
    )

    data_nascimento: Mapped[date | None] = mapped_column(
        Date
    )

    foto: Mapped[str | None] = mapped_column(
        String(500)
    )

    livros = relationship(
        "Livro",
        secondary=livro_autor,
        back_populates="autores"
    )