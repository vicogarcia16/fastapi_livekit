# Agente de Voz para LiveKit con FastAPI, Azure y ElevenLabs

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg?logo=python&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-RealTime-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)

> Un sofisticado asistente de voz en tiempo real para salas de LiveKit. Este proyecto proporciona una solución de backend completa, incluyendo un servidor FastAPI para la generación de tokens y un agente independiente que escucha, comprende y responde a los usuarios con una voz natural.

## ✨ Características Principales

*   **Backend con FastAPI:** Genera de forma segura tokens de acceso para que los clientes se unan a las salas de LiveKit.
*   **Agente de Voz en Tiempo Real:** Un worker que se une a las salas y actúa como un participante.
*   **Voz a Texto (STT):** Potenciado por **Azure Cognitive Speech Services** para una transcripción precisa.
*   **Respuestas Inteligentes (LLM):** Utiliza **Azure OpenAI** para comprender y generar respuestas similares a las humanas.
*   **Texto a Voz (TTS):** Emplea **ElevenLabs** para una síntesis de voz de alta calidad y sonido natural.
*   **Listo para Producción:** Incluye gestión de dependencias con Pipenv, herramientas de calidad de código con Ruff y un conjunto completo de pruebas con Pytest.

## 🏗️ Arquitectura

El proyecto se compone de dos servicios principales que se ejecutan de forma independiente:

1.  **Servidor FastAPI (`src/main.py`):**
    *   Su única responsabilidad es exponer un endpoint (`/api/v1/livekit/token`).
    *   Los clientes (ej. una aplicación web) le solicitan un token para poder conectarse a una sala de LiveKit.

2.  **Agente Worker (`src/services/agent_worker.py`):**
    *   Es un proceso independiente que se conecta directamente al servidor de LiveKit.
    *   Espera a que se le asigne un trabajo (unirse a una sala específica).
    *   Una vez en la sala, utiliza los servicios de Azure y ElevenLabs para escuchar, entender y hablar con los demás participantes.

## 📁 Estructura del Proyecto

La lógica de la aplicación se encuentra dentro del directorio `src` y sigue una organización modular:

```
src/
├── core/         # Lógica central: configuración (config.py), excepciones, etc.
├── routers/      # Endpoints de la API (token.py).
├── schemas/      # Modelos de datos Pydantic para las peticiones/respuestas (token.py).
├── services/     # Lógica de negocio: el agente, worker y configuración de IA.
└── main.py       # Punto de entrada de la aplicación FastAPI.
```

## 🚀 Guía de Inicio

### Prerrequisitos

*   Python 3.11+
*   `pipenv`
*   Cuentas y claves de API para:
    *   LiveKit
    *   Azure (Cognitive Services & OpenAI)
    *   ElevenLabs

### 1. Instalación

```sh
git clone <URL_DEL_REPOSITORIO>
cd fastapi_livekit
pipenv install --dev
pipenv shell
```

### 2. Configuración de Entorno

El proyecto carga las credenciales desde 4 archivos de entorno distintos. Deberás crearlos y rellenarlos con tus claves.

**1. Archivo General (`.env`)**

Crea un archivo llamado `.env` en la **raíz del proyecto**.

*Contenido de `.env`:*
```dotenv
LOG_LEVEL="INFO"
```

**2. Archivo de LiveKit (`env/.livekit.env`)**

Crea un archivo llamado `.livekit.env` dentro de la carpeta `env/`.

*Contenido de `env/.livekit.env`:*
```dotenv
LIVEKIT_API_KEY="API..."
LIVEKIT_API_SECRET="..."
LIVEKIT_URL="wss://..."
```

**3. Archivo de Azure (`env/.azure.env`)**

Crea un archivo llamado `.azure.env` dentro de la carpeta `env/`.

*Contenido de `env/.azure.env`:*
```dotenv
AZURE_SPEECH_KEY="..."
AZURE_SPEECH_REGION="..."
AZURE_OPENAI_API_KEY="..."
AZURE_OPENAI_ENDPOINT="https://..."
AZURE_OPENAI_DEPLOYMENT_NAME="..."
AZURE_OPENAI_API_VERSION="..."
```

**4. Archivo de ElevenLabs (`env/.elevenlabs.env`)**

Crea un archivo llamado `.elevenlabs.env` dentro de la carpeta `env/`.

*Contenido de `env/.elevenlabs.env`:*
```dotenv
ELEVENLABS_API_KEY="..."
VOICE_ID="..." # El ID de la voz de ElevenLabs que quieres que use el agente
```

## 🛠️ Uso

### Ejecutando el Servidor FastAPI

Este servidor proporciona el endpoint `/token`.

```sh
pipenv run server
```

### Ejecutando el Agente de Voz

Esto inicia el worker del agente, que se conectará a tu servidor de LiveKit y esperará a que se le asigne una sala.

```sh
pipenv run agente
```

## ✅ Testing

Este proyecto utiliza `pytest` para las pruebas unitarias y `ruff` para el linting y formateo.

*   **Ejecutar todas las pruebas con cobertura:**
    ```sh
    pipenv run test-cov
    ```
*   **Ejecutar el linter:**
    ```sh
    pipenv run lint
    ```
*   **Auto-formatear el código:**
    ```sh
    pipenv run format
    ```

## 📄 Licencia

Este proyecto está distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.