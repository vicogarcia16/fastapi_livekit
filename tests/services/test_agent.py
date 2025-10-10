from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.services.agent import MyAgent
from livekit.agents import AgentSession
from livekit.agents.worker import JobContext

# Usamos pytest.mark.anyio para todas las pruebas en este archivo
pytestmark = pytest.mark.anyio


class TestAgentLogic:
    """Pruebas unitarias para la lógica interna de MyAgent."""

    async def test_process_stt_final_speech(self):
        """Verifica que _process_stt produzca texto solo en eventos finales."""
        agent = MyAgent()
        mock_session = AsyncMock()

        stt_event_final = MagicMock()
        stt_event_final.is_final = True
        stt_event_final.text = "Hola mundo"

        stt_event_interim = MagicMock()
        stt_event_interim.is_final = False
        stt_event_interim.text = "Hola..."

        async def stt_gen():
            yield stt_event_interim
            yield stt_event_final

        mock_session.stt.stream = MagicMock(return_value=stt_gen())

        results = [text async for text in agent._process_stt(mock_session)]

        assert results == ["Hola mundo"]

    async def test_process_llm_stream(self):
        """Verifica que _process_llm procese el stream del LLM correctamente."""
        agent = MyAgent()
        mock_session = AsyncMock()
        input_text = "¿Qué tiempo hace?"

        llm_chunk1 = MagicMock()
        llm_chunk1.text = "Hace sol"
        llm_chunk2 = MagicMock()
        llm_chunk2.text = " y calor."

        async def llm_gen():
            yield llm_chunk1
            yield llm_chunk2

        mock_session.llm_stream = MagicMock(return_value=llm_gen())

        results = [text async for text in agent._process_llm(mock_session, input_text)]

        assert results == ["Hace sol", " y calor."]
        mock_session.llm_stream.assert_called_once_with(input_text)

    async def test_process_tts(self):
        """Verifica que _process_tts llame al motor de TTS con el texto correcto."""
        agent = MyAgent()
        mock_session = AsyncMock()

        async def text_stream():
            yield "Hola."
            yield " Adiós."

        await agent._process_tts(mock_session, text_stream())

        assert mock_session.out_audio.say.call_count == 2
        mock_session.out_audio.say.assert_any_call("Hola.")
        mock_session.out_audio.say.assert_any_call(" Adiós.")

    @patch.object(MyAgent, '_process_stt') # Patch with default MagicMock
    @patch.object(MyAgent, '_process_llm', new_callable=AsyncMock)
    @patch.object(MyAgent, '_process_tts', new_callable=AsyncMock)
    async def test_process_chat(self, mock_process_tts, mock_process_llm, mock_process_stt):
        """
        Verifica que _process_chat orqueste correctamente STT, LLM y TTS.
        """
        agent = MyAgent()
        mock_session = AsyncMock(spec=AgentSession)

        async def mock_stt_gen_func(*args, **kwargs):
            yield "user input"
        mock_process_stt.side_effect = mock_stt_gen_func

        # Configurar mock_process_llm para que devuelva un generador asíncrono
        async def mock_llm_gen():
            yield "llm response"
        mock_process_llm.return_value = mock_llm_gen()

        await agent._process_chat(mock_session)

        mock_process_stt.assert_called_once_with(mock_session)
        mock_process_llm.assert_called_once_with(mock_session, "user input")
        mock_process_tts.assert_called_once()

    @patch('src.services.agent.AgentSession', new_callable=MagicMock)
    @patch.object(MyAgent, '_process_chat', new_callable=AsyncMock)
    async def test_agent_entrypoint(self, mock_process_chat, MockAgentSession):
        """
        Verifica que agent_entrypoint inicialice la sesión y llame a _process_chat.
        """
        agent = MyAgent()
        mock_ctx = AsyncMock(spec=JobContext)
        mock_ctx.room.name = "test-room"
        mock_ctx.connect = AsyncMock()

        # Configurar el mock de AgentSession
        mock_session_instance = MockAgentSession.return_value
        mock_session_instance.start = AsyncMock()

        await agent.agent_entrypoint(mock_ctx)

        MockAgentSession.assert_called_once()
        mock_session_instance.start.assert_called_once_with(agent=agent, room=mock_ctx.room)
        mock_ctx.connect.assert_called_once()
        mock_process_chat.assert_called_once_with(mock_session_instance)