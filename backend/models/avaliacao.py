from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Avaliacao(Base):
    __tablename__ = "avaliacao"

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

    nota: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False
    )

    data_avaliacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    usuario = relationship(
        "Usuario",
        back_populates="avaliacoes"
    )

    livro = relationship(
        "Livro",
        back_populates="avaliacoes"
    )