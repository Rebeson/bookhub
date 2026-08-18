from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.database.connection import get_db


app = FastAPI(
    title="BookHub API",
    description="API REST do sistema BookHub",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "mensagem": "Bem-vindo à API do BookHub!"
    }


@app.get("/teste-banco")
def teste_banco(db: Session = Depends(get_db)):
    resultado = db.execute(text("SELECT 1"))
    
    return {
        "banco": "conectado",
        "resultado": resultado.scalar()
    }