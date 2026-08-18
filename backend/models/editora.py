from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Editora(Base):
    __tablename__ = "editora"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True
    )

    descricao: Mapped[str | None] = mapped_column(
        Text
    )

    site: Mapped[str | None] = mapped_column(
        String(500)
    )

    livros = relationship(
        "Livro",
        back_populates="editora"
    )