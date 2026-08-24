from datetime import datetime

from pydantic import BaseModel


class FavoritoResponse(BaseModel):
    usuario_id: int
    livro_id: int
    data_adicao: datetime

    class Config:
        from_attributes = True