import pytest
from httpx import AsyncClient


@pytest.mark.anyio
class TestTokenRouter:
    """Grupo de pruebas para el router de tokens."""

    async def test_generate_token(self, client: AsyncClient):
        """Verifica que el endpoint /token genere un token de acceso válido."""
        token_request_data = {
            "room_name": "test-room",
            "identity": "test-user",
            "name": "Test User",
            "metadata": '{"role": "tester"}',
        }

        response = await client.post("/api/v1/livekit/token", json=token_request_data)

        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["access_token"]

    async def test_generate_token_exception(self, client: AsyncClient, monkeypatch):
        """Verifica que se lance LiveKitTokenError si las credenciales son inválidas."""
        monkeypatch.setattr("src.routers.token.settings.livekit.LIVEKIT_API_KEY", "")
        monkeypatch.setattr("src.routers.token.settings.livekit.LIVEKIT_API_SECRET", "")

        token_request_data = {
            "room_name": "test-room",
            "identity": "test-user",
            "name": "Test User",
            "metadata": '{"role": "tester"}',
        }

        # El router de FastAPI maneja la excepción y devuelve un error HTTP.
        # No podemos usar pytest.raises directamente en el cliente HTTP.
        # En su lugar, verificamos que la respuesta sea un error 500.
        response = await client.post("/api/v1/livekit/token", json=token_request_data)

        assert response.status_code == 500
        response_data = response.json()
        assert "detail" in response_data
        assert "Could not generate LiveKit token" in response_data["detail"]
