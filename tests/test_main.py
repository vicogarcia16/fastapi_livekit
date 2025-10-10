import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_healthcheck(client: AsyncClient):
    """Verifica que el endpoint /healthcheck funcione correctamente."""
    response = await client.get("/api/v1/healthcheck")

    # Verifica que la respuesta sea exitosa (200 OK)
    assert response.status_code == 200

    # Verifica el contenido de la respuesta
    assert response.json() == {"status": "ok"}
