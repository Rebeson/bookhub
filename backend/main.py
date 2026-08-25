from fastapi import FastAPI
from backend.routers.auth import router as auth_router
from backend.routers.usuarios import router as usuarios_router
from backend.routers.livros import router as livros_router
from backend.routers.estante import router as estante_router
from backend.routers.autores import router as autores_router
from backend.routers.generos import router as generos_router
from backend.routers.avaliacoes import router as avaliacoes_router
from backend.routers.favoritos import router as favoritos_router
from backend.routers.resenhas import router as resenhas_router


app = FastAPI(
    title="BookHub API",
    description="API REST do sistema BookHub",
    version="1.0.0"
)


app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(livros_router)
app.include_router(autores_router)
app.include_router(generos_router)
app.include_router(estante_router)
app.include_router(avaliacoes_router)
app.include_router(favoritos_router)
app.include_router(resenhas_router)


@app.get("/")
def raiz():
    return {
        "mensagem": "BookHub API funcionando!"
    }