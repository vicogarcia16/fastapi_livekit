"""
Punto de entrada principal de la aplicación FastAPI.

Este módulo configura la aplicación FastAPI, incluyendo sus routers, manejadores
de excepciones y el ciclo de vida (lifespan) para la gestión de recursos.
También define un endpoint de health check.
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.config import settings
from .core.exception_handlers import add_exception_handlers
from .routers import token


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación FastAPI.

    Actualmente, silencia las excepciones de cancelación e interrupción
    para permitir un apagado más limpio de la aplicación.

    Args:
        app: La instancia de la aplicación FastAPI.
    """
    try:  # pragma: no cover
        yield
    except (asyncio.CancelledError, KeyboardInterrupt):  # pragma: no cover
        # ? Silenciar excepciones de cancelación/interrupción
        pass


app = FastAPI(
    title=settings.app.APP_NAME,
    description=settings.app.APP_DESCRIPTION,
    contact=settings.app.APP_CONTACT.model_dump(),
    version=settings.app.APP_VERSION,
    docs_url=settings.app.APP_DOCS_URL,
    redoc_url=settings.app.APP_REDOC_URL,
    openapi_url=f"{settings.app.api_prefix}/openapi.json",
    lifespan=lifespan,
)

# Añadir manejadores de excepciones
add_exception_handlers(app)

app.include_router(token.router, prefix=settings.app.api_prefix)


@app.get(f"{settings.app.api_prefix}/healthcheck", tags=["Monitoring"])
async def healthcheck():
    """
    Endpoint de health check para verificar el estado de la aplicación.

    Returns:
        dict: Un diccionario con el estado de la aplicación.
    """
    return {"status": "ok"}
