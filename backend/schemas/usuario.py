from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    nome: str = Field(
        min_length=1,
        max_length=100
    )

    nome_usuario: str = Field(
        min_length=3,
        max_length=50
    )

    email: EmailStr

    foto_perfil: str | None = None

    biografia: str | None = None


class UsuarioCreate(UsuarioBase):
    senha: str = Field(
        min_length=6,
        max_length=100
    )


class UsuarioResponse(UsuarioBase):
    id: int
    data_cadastro: datetime
    tipo_usuario: str
    ativo: bool

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        max_length=100
    )

    nome_usuario: str | None = Field(
        default=None,
        max_length=50
    )

    email: EmailStr | None = None

    foto_perfil: str | None = Field(
        default=None,
        max_length=500
    )

    biografia: str | None = None