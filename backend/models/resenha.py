from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Resenha(Base):
    __tablename__ = "resenha"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False
    )

    livro_id: Mapped[int] = mapped_column(
        ForeignKey("livro.id"),
        nullable=False
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    conteudo: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    data_publicacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    usuario = relationship(
        "Usuario",
        back_populates="resenhas"
    )

    livro = relationship(
        "Livro",
        back_populates="resenhas"
    )