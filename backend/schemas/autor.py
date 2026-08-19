from datetime import date

from pydantic import BaseModel, ConfigDict


class AutorBase(BaseModel):
    nome: str
    biografia: str | None = None
    data_nascimento: date | None = None
    foto: str | None = None


class AutorCreate(AutorBase):
    pass


class AutorUpdate(BaseModel):
    nome: str | None = None
    biografia: str | None = None
    data_nascimento: date | None = None
    foto: str | None = None


class AutorResponse(AutorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)