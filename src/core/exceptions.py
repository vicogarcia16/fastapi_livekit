"""
Define las clases de excepciones personalizadas para la aplicación.

Estas excepciones heredan de `fastapi.HTTPException`, lo que permite que sean
manejadas globalmente por los manejadores de excepciones de FastAPI y se
traduzcan automáticamente en respuestas de error HTTP.
"""

from fastapi import status


class LiveKitTokenError(Exception):
    """Se lanza cuando ocurre un error durante la generación de un token de LiveKit."""

    def __init__(self, message: str = "No se pudo generar el token de LiveKit"):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message
        super().__init__(self.message)


class AgentError(Exception):
    """Se lanza cuando ocurre un error relacionado con el agente de LiveKit."""

    def __init__(self, message: str = "Ocurrió un error en el agente"):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.message = message
        super().__init__(self.message)
