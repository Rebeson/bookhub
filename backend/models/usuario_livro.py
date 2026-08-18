from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UsuarioLivro(Base):
    __tablename__ = "usuario_livro"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        primary_key=True
    )

    livro_id: Mapped[int] = mapped_column(
        ForeignKey("livro.id"),
        primary_key=True
    )

    status_leitura: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    pagina_atual: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    data_adicao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    data_inicio: Mapped[date | None] = mapped_column(
        Date
    )

    data_conclusao: Mapped[date | None] = mapped_column(
        Date
    )

    usuario = relationship(
        "Usuario",
        back_populates="livros"
    )

    livro = relationship(
        "Livro",
        back_populates="usuarios"
    )