import sys
from pathlib import Path

# `_parallel` uses package-relative imports (`from .models import ...`), so it
# must be imported as `websearch._parallel` rather than a bare top-level module.
sys.path.insert(0, str(Path(__file__).parent.parent))

from websearch._parallel import MCP_CLIENT_NAME, ParallelBackend


def test_mcp_headers_send_identifiable_user_agent():
    backend = ParallelBackend(api_key=None)

    headers = backend._mcp_headers(None)

    # Free MCP traffic is identifiable at the HTTP layer, not just via clientInfo.
    assert headers["User-Agent"].startswith(f"{MCP_CLIENT_NAME}/")
    # Anonymous free path: no bearer token.
    assert "Authorization" not in headers


def test_mcp_headers_keep_user_agent_with_session_id():
    backend = ParallelBackend(api_key=None)

    headers = backend._mcp_headers("sess-123")

    assert headers["Mcp-Session-Id"] == "sess-123"
    assert headers["User-Agent"].startswith(f"{MCP_CLIENT_NAME}/")
