# API для сайта «Шах Lounge». Запуск: uvicorn app.main:app --port 8000
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import load_settings
from .iiko import IikoError
from .tables import TablesService

settings = load_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.tables = TablesService(settings)
    yield
    await app.state.tables.close()


app = FastAPI(title="Шах Lounge API", lifespan=lifespan, docs_url="/api/docs", openapi_url="/api/openapi.json")

if settings.cors_origins:
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["GET"], allow_headers=["*"])


@app.get("/api/health")
async def health():
    return {"ok": True, "demo": settings.demo}


@app.get("/api/tables")
async def tables():
    """Столы и их статусы: free — свободен, busy — занят, reserved — забронирован."""
    try:
        return await app.state.tables.get()
    except IikoError as e:
        raise HTTPException(503, f"Нет данных из iiko: {e}") from e
