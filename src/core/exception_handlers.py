"""
Define los manejadores de excepciones globales para la aplicación FastAPI.

Estos manejadores capturan excepciones específicas (y genéricas) y las convierten
en respuestas JSON estandarizadas, asegurando que los errores de la API sean
consistentes y predecibles para el cliente.
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from .exceptions import AgentError, LiveKitTokenError


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manejador para las excepciones HTTPException estándar de FastAPI.

    Args:
        request: El objeto de la solicitud entrante.
        exc: La instancia de la excepción HTTPException.

    Returns:
        Una respuesta JSON con el código de estado y el detalle del error.
    """
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.detail or "HTTP Error"}
    )


async def livekit_token_error_handler(request: Request, exc: LiveKitTokenError):
    """
    Manejador para la excepción personalizada LiveKitTokenError.

    Args:
        request: El objeto de la solicitud entrante.
        exc: La instancia de la excepción LiveKitTokenError.

    Returns:
        Una respuesta JSON con el código de estado y el mensaje de la excepción.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def agent_error_handler(request: Request, exc: AgentError):
    """
    Manejador para la excepción personalizada AgentError.

    Args:
        request: El objeto de la solicitud entrante.
        exc: La instancia de la excepción AgentError.

    Returns:
        Una respuesta JSON con el código de estado y el mensaje de la excepción.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Manejador genérico para cualquier excepción no capturada.

    Esto previene que errores inesperados filtren información sensible y devuelve
    una respuesta de error 500 estandarizada.

    Args:
        request: El objeto de la solicitud entrante.
        exc: La instancia de la excepción genérica.

    Returns:
        Una respuesta JSON de error 500 Internal Server Error.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected internal server error occurred."},
    )


def add_exception_handlers(app: FastAPI):
    """
    Añade todos los manejadores de excepciones personalizados a la aplicación FastAPI.

    Args:
        app: La instancia de la aplicación FastAPI.
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(LiveKitTokenError, livekit_token_error_handler)
    app.add_exception_handler(AgentError, agent_error_handler)
    # El manejador genérico debe ir al final como un "catch-all"
    app.add_exception_handler(Exception, generic_exception_handler)
