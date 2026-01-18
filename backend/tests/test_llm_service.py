"""
Unit tests for LLM service with mocked OpenAI client.
"""
import pytest
import json
from unittest.mock import MagicMock, patch, AsyncMock
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))


class MockDelta:
    """Mock for OpenAI streaming delta."""
    def __init__(self, content=None, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls


class MockChoice:
    """Mock for OpenAI streaming choice."""
    def __init__(self, delta):
        self.delta = delta


class MockChunk:
    """Mock for OpenAI streaming chunk."""
    def __init__(self, delta):
        self.choices = [MockChoice(delta)]


class MockToolCall:
    """Mock for OpenAI tool call."""
    def __init__(self, arguments):
        self.function = MagicMock()
        self.function.arguments = arguments


def create_text_chunks(text_parts):
    """Create mock chunks for text response."""
    return [MockChunk(MockDelta(content=part)) for part in text_parts]


def create_tool_chunks(argument_parts):
    """Create mock chunks for tool call response."""
    return [
        MockChunk(MockDelta(tool_calls=[MockToolCall(part)]))
        for part in argument_parts
    ]


class TestStreamChat:
    """Tests for the stream_chat function."""

    @pytest.mark.asyncio
    async def test_stream_chat_text_response(self):
        """Verify text chunks are yielded correctly."""
        from core.llm import stream_chat, SYSTEM_PROMPT
        
        text_parts = ["Hello", ", ", "world", "!"]
        mock_chunks = create_text_chunks(text_parts)
        
        mock_response = MagicMock()
        mock_response.__iter__ = lambda self: iter(mock_chunks)
        
        with patch("core.llm.client.chat.completions.create", return_value=mock_response):
            messages = [{"role": "user", "content": "Say hello"}]
            
            chunks = []
            async for chunk in stream_chat(messages):
                chunks.append(chunk)
            
            assert len(chunks) == 4
            
            # Parse and verify content
            parsed = [json.loads(c) for c in chunks]
            assert all(p["type"] == "text" for p in parsed)
            assert "".join(p["content"] for p in parsed) == "Hello, world!"

    @pytest.mark.asyncio
    async def test_stream_chat_tool_call_response(self):
        """Verify tool call chunks are handled correctly."""
        from core.llm import stream_chat
        
        # Simulate tool call arguments coming in chunks
        arg_parts = ['{"title":', '"Test Plan",', '"steps": []}']
        mock_chunks = create_tool_chunks(arg_parts)
        
        mock_response = MagicMock()
        mock_response.__iter__ = lambda self: iter(mock_chunks)
        
        with patch("core.llm.client.chat.completions.create", return_value=mock_response):
            messages = [{"role": "user", "content": "Create a plan"}]
            
            chunks = []
            async for chunk in stream_chat(messages):
                chunks.append(chunk)
            
            assert len(chunks) == 3
            
            # Parse and verify tool chunks
            parsed = [json.loads(c) for c in chunks]
            assert all(p["type"] == "tool_chunk" for p in parsed)

    @pytest.mark.asyncio
    async def test_stream_chat_includes_system_prompt(self):
        """Verify system prompt is prepended to messages."""
        from core.llm import stream_chat, SYSTEM_PROMPT
        
        mock_response = MagicMock()
        mock_response.__iter__ = lambda self: iter([])
        
        with patch("core.llm.client.chat.completions.create", return_value=mock_response) as mock_create:
            messages = [{"role": "user", "content": "Hello"}]
            
            # Consume the generator
            async for _ in stream_chat(messages):
                pass
            
            # Verify the call was made with system prompt
            call_kwargs = mock_create.call_args.kwargs
            sent_messages = call_kwargs["messages"]
            
            assert sent_messages[0]["role"] == "system"
            assert sent_messages[0]["content"] == SYSTEM_PROMPT
            assert sent_messages[1] == messages[0]

    @pytest.mark.asyncio
    async def test_stream_chat_uses_correct_model(self):
        """Verify correct model is used."""
        from core.llm import stream_chat
        
        mock_response = MagicMock()
        mock_response.__iter__ = lambda self: iter([])
        
        with patch("core.llm.client.chat.completions.create", return_value=mock_response) as mock_create:
            async for _ in stream_chat([{"role": "user", "content": "Hi"}]):
                pass
            
            call_kwargs = mock_create.call_args.kwargs
            assert call_kwargs["model"] == "gpt-4o"
            assert call_kwargs["stream"] is True

    @pytest.mark.asyncio
    async def test_stream_chat_mixed_response(self):
        """Verify handling of mixed text and tool call responses."""
        from core.llm import stream_chat
        
        # Simulate: text first, then tool call
        mock_chunks = [
            MockChunk(MockDelta(content="I'll create a plan. ")),
            MockChunk(MockDelta(tool_calls=[MockToolCall('{"title": "Plan"}')])),
        ]
        
        mock_response = MagicMock()
        mock_response.__iter__ = lambda self: iter(mock_chunks)
        
        with patch("core.llm.client.chat.completions.create", return_value=mock_response):
            messages = [{"role": "user", "content": "Make a plan"}]
            
            chunks = []
            async for chunk in stream_chat(messages):
                chunks.append(json.loads(chunk))
            
            assert len(chunks) == 2
            assert chunks[0]["type"] == "text"
            assert chunks[1]["type"] == "tool_chunk"
