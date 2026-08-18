from sqlalchemy import Column, ForeignKey, Integer, Table

from .base import Base


livro_autor = Table(
    "livro_autor",
    Base.metadata,
    Column(
        "livro_id",
        Integer,
        ForeignKey("livro.id"),
        primary_key=True
    ),
    Column(
        "autor_id",
        Integer,
        ForeignKey("autor.id"),
        primary_key=True
    )
)


livro_genero = Table(
    "livro_genero",
    Base.metadata,
    Column(
        "livro_id",
        Integer,
        ForeignKey("livro.id"),
        primary_key=True
    ),
    Column(
        "genero_id",
        Integer,
        ForeignKey("genero.id"),
        primary_key=True
    )
)