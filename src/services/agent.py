"""
Define la lógica principal y el ciclo de vida del agente de voz de LiveKit.

Este módulo contiene la clase `MyAgent`, que hereda de `livekit.agents.Agent`
y orquesta el flujo de procesamiento de audio: STT -> LLM -> TTS.
"""

import logging

from livekit.agents import Agent, AgentSession
from livekit.agents.worker import JobContext

from src.core.config import settings
from src.services.agent_config import llm, stt, tts

logger = logging.getLogger("agent")


class MyAgent(Agent):
    """
    Agente de voz que transcribe la entrada del usuario, genera una respuesta con un LLM
    y la sintetiza de nuevo a voz.
    """

    def __init__(self):
        """Inicializa el agente con las instrucciones del sistema para el LLM."""
        super().__init__(instructions=settings.agent.INSTRUCTIONS)

    async def _process_stt(self, session: AgentSession):
        """
        Procesa el stream de audio del STT y produce texto finalizado.

        Args:
            session: La sesión actual del agente.

        Yields:
            str: El texto transcrito final de la entrada de voz.
        """
        async for speech_event in session.stt.stream():
            if speech_event.is_final:
                yield speech_event.text

    async def _process_llm(self, session: AgentSession, text: str):
        """
        Envía el texto al LLM y produce la respuesta en fragmentos (streaming).

        Args:
            session: La sesión actual del agente.
            text: El texto de entrada para el LLM.

        Yields:
            str: Fragmentos de la respuesta generada por el LLM.
        """
        llm_stream = session.llm_stream(text)
        async for chunk in llm_stream:
            if chunk.text:
                yield chunk.text

    async def _process_tts(self, session: AgentSession, text_stream):
        """
        Consume un stream de texto y lo sintetiza a audio, reproduciéndolo en la sala.

        Args:
            session: La sesión actual del agente.
            text_stream: Un generador asíncrono que produce fragmentos de texto.
        """
        async for text in text_stream:
            await session.out_audio.say(text)

    async def _process_chat(self, session: AgentSession):
        """
        Orquesta el ciclo de chat: STT -> LLM -> TTS.

        Args:
            session: La sesión actual del agente.
        """
        async for user_input in self._process_stt(session):
            logger.info(f"Usuario: {user_input}")

            llm_stream = self._process_llm(session, user_input)
            await self._process_tts(session, llm_stream)

    async def agent_entrypoint(self, ctx: JobContext):
        """
        Punto de entrada principal que se ejecuta cuando el worker recibe un trabajo.

        Gestiona la conexión a la sala, la inicialización de la sesión y el inicio
        del ciclo de procesamiento de chat.

        Args:
            ctx: El contexto del trabajo, proporcionado por el worker de LiveKit.
        """
        logger.info(f"Agente conectado a la sala: {ctx.room.name}")

        session = AgentSession(stt=stt, tts=tts, llm=llm)

        async with session:  # Usamos async with para gestionar la sesión
            await session.start(
                agent=self,
                room=ctx.room,
            )

            await ctx.connect()

            logger.info("Agente listo para escuchar y responder.")
            await self._process_chat(session)
