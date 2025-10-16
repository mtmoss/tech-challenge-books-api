from fastapi import FastAPI

app = FastAPI(
    title="Books API - Tech Challenge",
    version="0.1.0",
    description="API pública para consulta de livros (Fase 1).",
)

@app.get("/health")
def health_check():
    """
    Objetivo: endpoint simples para checar se a API está de pé.
    Retorna um JSON com status.
    """
    return {"status": "ok"}