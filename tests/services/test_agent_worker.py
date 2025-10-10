from unittest.mock import AsyncMock, MagicMock, patch
import pytest

# Importar la función que queremos probar
from src.services.agent_worker import entrypoint_function

# Importar las clases que necesitamos mockear
from src.services.agent import MyAgent
from livekit.agents.worker import JobContext

pytestmark = pytest.mark.anyio

class TestAgentWorker:
    """Pruebas unitarias para el worker del agente."""

    @patch('src.services.agent_worker.MyAgent')
    async def test_entrypoint_function(self, MockMyAgent):
        """
        Verifica que entrypoint_function instancie MyAgent y llame a agent_entrypoint.
        """
        # Configurar el mock para MyAgent
        mock_agent_instance = MockMyAgent.return_value
        mock_agent_instance.agent_entrypoint = AsyncMock()

        # Crear un mock para JobContext
        mock_job_context = AsyncMock(spec=JobContext)

        # Llamar a la función que estamos probando
        await entrypoint_function(mock_job_context)

        # Afirmar que MyAgent fue instanciado
        MockMyAgent.assert_called_once()

        # Afirmar que agent_entrypoint fue llamado con el contexto correcto
        mock_agent_instance.agent_entrypoint.assert_called_once_with(mock_job_context)
