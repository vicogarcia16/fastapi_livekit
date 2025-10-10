import json
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.core.exception_handlers import (
    agent_error_handler,
    generic_exception_handler,
    http_exception_handler,
    livekit_token_error_handler,
)
from src.core.exceptions import AgentError, LiveKitTokenError


@pytest.mark.anyio
class TestExceptionHandlers:
    async def test_http_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="I'm a teapot"
        )
        response = await http_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_418_IM_A_TEAPOT
        assert json.loads(response.body) == {"detail": "I'm a teapot"}

    async def test_http_exception_handler_no_detail(self):
        request = MagicMock(spec=Request)
        exc = HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail=None)
        response = await http_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_418_IM_A_TEAPOT
        assert json.loads(response.body) == {"detail": "I'm a Teapot"}

    async def test_generic_exception_handler(self):
        request = MagicMock(spec=Request)
        exc = ValueError("Something unexpected happened")
        response = await generic_exception_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert json.loads(response.body) == {
            "detail": "An unexpected internal server error occurred."
        }

    async def test_livekit_token_error_handler(self):
        request = MagicMock(spec=Request)
        exc = LiveKitTokenError("Invalid token")
        response = await livekit_token_error_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert json.loads(response.body) == {"detail": "Invalid token"}

    async def test_agent_error_handler(self):
        request = MagicMock(spec=Request)
        exc = AgentError("Agent error")
        response = await agent_error_handler(request, exc)
        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert json.loads(response.body) == {"detail": "Agent error"}
