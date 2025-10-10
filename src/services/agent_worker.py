"""
Lanza el proceso trabajador (worker) del agente de LiveKit.

Este script es el punto de entrada para ejecutar el agente como un servicio
independiente. Se conecta a LiveKit y espera a que se le asignen trabajos (salas).

Para ejecutarlo, usa el comando:
`python -m src.services.agent_worker`
"""

import logging

from livekit.agents import WorkerOptions, cli
from livekit.agents.worker import JobContext

from src.core.config import settings
from src.services.agent import MyAgent

# Configuración de logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("agent")


async def entrypoint_function(ctx: JobContext):
    """
    Función de entrada que el worker de LiveKit llama para cada trabajo.

    Crea una instancia de `MyAgent` y delega el control al punto de entrada
    del agente (`agent_entrypoint`).

    Args:
        ctx: El contexto del trabajo, proporcionado por el worker.
    """
    agent_instance = MyAgent()
    await agent_instance.agent_entrypoint(ctx)


if __name__ == "__main__":  # pragma: no cover
    logger.info("Iniciando worker del agente...")

    cli.run_app(  # pragma: no cover
        WorkerOptions(
            entrypoint_fnc=entrypoint_function,
            api_key=settings.livekit.LIVEKIT_API_KEY,
            api_secret=settings.livekit.LIVEKIT_API_SECRET,
            ws_url=settings.livekit.LIVEKIT_URL,
        )
    )
