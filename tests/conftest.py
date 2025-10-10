import asyncio
from asyncio import SelectorEventLoop
from contextlib import asynccontextmanager

import pytest


@pytest.fixture
def anyio_backend():
    return "asyncio"


# === Fuerza SelectorEventLoop en Windows ===


@pytest.fixture(scope="function", autouse=True)
def event_loop():
    try:
        from asyncio import WindowsSelectorEventLoopPolicy

        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    except ImportError:
        pass

    loop = SelectorEventLoop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# === Desactiva lifespan de FastAPI ===
@asynccontextmanager
async def null_lifespan(app):
    yield


# === Cliente de prueba ===
@pytest.fixture(scope="function")
async def client():
    from src.main import app

    # Desactiva el lifespan
    app.router.lifespan_context = null_lifespan

    from httpx import ASGITransport, AsyncClient

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
