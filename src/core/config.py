"""
Configuración centralizada de la aplicación.

Este módulo utiliza Pydantic Settings para cargar y gestionar la configuración
desde archivos .env y variables de entorno. Centraliza todas las variables
necesarias para los servicios de LiveKit, Azure, ElevenLabs y la propia
aplicación FastAPI.
"""

import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# Construye la ruta a la carpeta 'env' que está en el directorio raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_dir = os.path.join(ROOT_DIR, "env")


class LiveKitSettings(BaseSettings):
    """Configuración específica para el servicio de LiveKit."""

    # Carga variables desde el archivo .livekit.env
    model_config = SettingsConfigDict(
        env_file=os.path.join(env_dir, ".livekit.env"), extra="ignore"
    )

    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_URL: str  # Debería ser tu WS/WSS URL


class AzureSettings(BaseSettings):
    """Configuración para los servicios de Azure (Speech y OpenAI)."""

    # Carga variables desde el archivo .azure.env
    model_config = SettingsConfigDict(
        env_file=os.path.join(env_dir, ".azure.env"), extra="ignore"
    )

    # Estas dos variables faltaban en tu archivo:
    AZURE_SPEECH_KEY: str
    AZURE_SPEECH_REGION: str

    # Estas ya las tenías:
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: (
        str  # Nueva variable para la versión de la API de OpenAI en Azure
    )


class ElevenLabsSettings(BaseSettings):
    """Configuración para el servicio de Text-to-Speech de ElevenLabs."""

    # Carga variables desde el archivo .elevenlabs.env
    model_config = SettingsConfigDict(
        env_file=os.path.join(env_dir, ".elevenlabs.env"), extra="ignore"
    )

    ELEVENLABS_API_KEY: str

    # Esta variable faltaba en tu archivo:
    VOICE_ID: str


class AgentSettings(BaseSettings):
    """Configuración de comportamiento para el agente de LiveKit."""

    INSTRUCTIONS: str = "Eres un asistente de voz útil. Responde a las preguntas de los usuarios de forma concisa y clara."


class Contact(BaseSettings):
    """Define los datos de contacto para la documentación de la API."""

    name: str
    url: str


class AppSettings(BaseSettings):
    """Configuración general de la aplicación FastAPI y su documentación."""

    APP_NAME: str = "LiveKit Agent Voice con Azure y ElevenLabs"
    APP_DESCRIPTION: str = "Un agente de voz de LiveKit que utiliza Azure para STT, ElevenLabs para TTS y Azure OpenAI para LLM."
    APP_VERSION: str = "1"
    APP_CONTACT: Contact = Contact(
        name="Víctor García", url="https://github.com/vicogarcia16"
    )
    APP_DOCS_URL: str = "/"
    APP_REDOC_URL: str = "/redoc"

    @property
    def api_prefix(self):  # pragma: no cover
        """Prefijo para todas las rutas de la API, basado en la versión."""
        return f"/api/v{self.APP_VERSION}"

    @property
    def api_version(self):  # pragma: no cover
        """Versión de la API para la documentación OpenAPI."""
        return f"{self.APP_VERSION}.0.0"


class Settings(BaseSettings):
    """Clase principal que agrega y gestiona toda la configuración de la aplicación."""

    # Carga variables desde el archivo .env en la raíz del proyecto
    model_config = SettingsConfigDict(
        env_file=os.path.join(ROOT_DIR, ".env"), extra="ignore"
    )

    LOG_LEVEL: str
    livekit: LiveKitSettings = LiveKitSettings()
    azure: AzureSettings = AzureSettings()
    elevenlabs: ElevenLabsSettings = ElevenLabsSettings()
    agent: AgentSettings = AgentSettings()
    app: AppSettings = AppSettings()


# Objeto global de configuración para ser usado en toda la aplicación
settings = Settings()
