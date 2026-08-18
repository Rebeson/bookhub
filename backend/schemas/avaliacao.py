from datetime import datetime

from pydantic import BaseModel, Field


class AvaliacaoCreate(BaseModel):
    livro_id: int

    nota: int = Field(
        ge=1,
        le=5
    )


class AvaliacaoUpdate(BaseModel):
    nota: int = Field(
        ge=1,
        le=5
    )


class AvaliacaoResponse(BaseModel):
    id: int
    usuario_id: int
    livro_id: int
    nota: int
    data_avaliacao: datetime
    data_atualizacao: datetime

    class Config:
        from_attributes = True