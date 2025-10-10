"""
Define los schemas de Pydantic para la validación de datos en las rutas de token.

Estos modelos son utilizados por FastAPI para validar, serializar y documentar
automáticamente los cuerpos de las solicitudes (request bodies) en la API.
"""

from typing import Optional

from pydantic import BaseModel


class TokenRequest(BaseModel):
    """
    Schema para la solicitud de creación de un token de acceso de LiveKit.

    Atributos:
        room_name (str): El nombre de la sala a la que se unirá el participante.
        identity (str): La identidad única del participante.
        name (Optional[str]): El nombre visible del participante en la sala.
        metadata (Optional[str]): Metadatos personalizados para asociar al participante.
    """

    room_name: str
    identity: str
    name: Optional[str] = None
    metadata: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "room_name": "nombre-de-la-sala",
                    "identity": "identidad-unica-del-usuario",
                    "name": "Nombre del Usuario",
                    "metadata": '{"user_id": 123, "rol": "moderador"}',
                }
            ]
        }
    }
