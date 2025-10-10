"""
Configuración e inicialización de los servicios de Agentes de LiveKit.

Este módulo se encarga de instanciar los servicios de STT (Speech-to-Text),
TTS (Text-to-Speech), y LLM (Large Language Model) utilizando la configuración
proveída a través de las variables de entorno y cargada en `core.config`.

Servicios instanciados:
- stt: Servicio de Azure para la transcripción de voz a texto.
- tts: Servicio de ElevenLabs para la síntesis de texto a voz.
- llm: Modelo de lenguaje de Azure OpenAI para la generación de respuestas.
"""

import logging

from livekit.plugins import azure, elevenlabs, openai

from src.core.config import settings

logger = logging.getLogger("agent")

# Inicialización de los servicios de STT y TTS
stt = azure.STT(  # pragma: no cover
    language="es-ES",
    speech_key=settings.azure.AZURE_SPEECH_KEY,
    speech_region=settings.azure.AZURE_SPEECH_REGION,
)
tts = elevenlabs.TTS(  # pragma: no cover
    api_key=settings.elevenlabs.ELEVENLABS_API_KEY,
    voice_id=settings.elevenlabs.VOICE_ID,
)
logger.info(f"ElevenLabs TTS inicializado con VOICE_ID: {settings.elevenlabs.VOICE_ID}")

# Inicialización del LLM de Azure OpenAI
llm = openai.realtime.RealtimeModel.with_azure(  # pragma: no cover
    azure_deployment=settings.azure.AZURE_OPENAI_DEPLOYMENT_NAME,
    api_version=settings.azure.AZURE_OPENAI_API_VERSION,
    api_key=settings.azure.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.azure.AZURE_OPENAI_ENDPOINT,
)
