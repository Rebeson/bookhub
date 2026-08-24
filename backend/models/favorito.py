from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Favorito(Base):
    __tablename__ = "favorito"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        primary_key=True
    )

    livro_id: Mapped[int] = mapped_column(
        ForeignKey("livro.id"),
        primary_key=True
    )

    data_adicao: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    usuario = relationship(
        "Usuario",
        back_populates="favoritos"
    )

    livro = relationship(
        "Livro",
        back_populates="favoritos"
    )