from enum import Enum

from pydantic import BaseModel, Field


class StatusLeitura(str, Enum):
    QUERO_LER = "QUERO_LER"
    LENDO = "LENDO"
    LIDO = "LIDO"


class EstanteAtualizacao(BaseModel):
    status_leitura: StatusLeitura
    pagina_atual: int = Field(ge=0)