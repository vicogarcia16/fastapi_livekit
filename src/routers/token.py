"""
Define las rutas de la API para las operaciones relacionadas con LiveKit.

Actualmente, contiene la ruta para generar tokens de acceso para que los
clientes se conecten a las salas de LiveKit.
"""

from fastapi import APIRouter
from livekit.api import AccessToken, VideoGrants

from src.core.config import settings
from src.core.exceptions import LiveKitTokenError
from src.schemas.token import TokenRequest

router = APIRouter(
    prefix="/livekit",
    tags=["LiveKit"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=dict[str, str])
async def token(request: TokenRequest):
    """
    Genera un token de acceso (JWT) de LiveKit para un participante.

    Este token es necesario para que un cliente se autentique y se una a una sala.

    Args:
        request: Un objeto `TokenRequest` con los detalles del participante.

    Returns:
        Un diccionario que contiene el `access_token` JWT.

    Raises:
        LiveKitTokenError: Si ocurre un error durante la generación del token.
    """
    try:
        token = (
            AccessToken(
                settings.livekit.LIVEKIT_API_KEY,
                settings.livekit.LIVEKIT_API_SECRET,
            )
            .with_identity(request.identity)
            .with_name(request.name)
            .with_metadata(request.metadata)
            .with_grants(VideoGrants(room=request.room_name, room_join=True))
        )
        return {"access_token": token.to_jwt()}
    except Exception as e:
        raise LiveKitTokenError(f"Could not generate LiveKit token: {e}") from e
