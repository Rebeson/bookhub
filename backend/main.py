from fastapi import FastAPI
from backend.routers.auth import router as auth_router
from backend.routers.usuarios import router as usuarios_router
from backend.routers.livros import router as livros_router
from backend.routers.autores import router as autores_router


app = FastAPI(
    title="BookHub API",
    description="API REST do sistema BookHub",
    version="1.0.0"
)


app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(livros_router)
app.include_router(autores_router)


@app.get("/")
def raiz():
    return {
        "mensagem": "BookHub API funcionando!"
    }