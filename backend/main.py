from fastapi import FastAPI
from backend.routers.auth import router as auth_router
from backend.routers.usuarios import router as usuarios_router


app = FastAPI(
    title="BookHub API",
    description="API REST do sistema BookHub",
    version="1.0.0"
)


app.include_router(usuarios_router)
app.include_router(auth_router)


@app.get("/")
def raiz():
    return {
        "mensagem": "BookHub API funcionando!"
    }