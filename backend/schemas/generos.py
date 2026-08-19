from pydantic import BaseModel, ConfigDict


class GeneroBase(BaseModel):
    nome: str
    descricao: str | None = None


class GeneroCreate(GeneroBase):
    pass


class GeneroUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None


class GeneroResponse(GeneroBase):
    id: int

    model_config = ConfigDict(from_attributes=True)