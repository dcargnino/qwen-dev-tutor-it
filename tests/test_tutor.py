from __future__ import annotations

from unittest import mock

import pytest

from qwen_dev_tutor.client import ChatResult, QwenClientError
from qwen_dev_tutor.config import AppConfig
from qwen_dev_tutor.tutor import (
    run_chat,
    run_chat_async,
    run_code_tutor,
    run_code_tutor_async,
    run_vision_async,
)

# ── fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def fake_config() -> AppConfig:
    return AppConfig(
        provider="test-provider",
        api_key="test-key",
        base_url="http://test:8000",
        model="qwen-test",
        timeout_seconds=10,
    )


@pytest.fixture
def fake_chat_result() -> ChatResult:
    return ChatResult(
        content="risposta di test",
        model="qwen-test",
        provider="test-provider",
        raw_response={},
    )


# Shared expected content copied from prompts.py so tests are self-explanatory.
_CHAT_SYSTEM_CONTENT = (
    "Sei Qwen, un assistente utile per sviluppatori. "
    "Rispondi in italiano in modo chiaro, concreto e sintetico."
)

# ── run_chat ───────────────────────────────────────────────────────────────────


class TestRunChat:
    """Tests for the synchronous ``run_chat`` function."""

    def test_calls_client_chat_with_chat_messages(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """run_chat creates an OpenAICompatibleClient and delegates to
        client.chat() with messages built by build_chat_messages."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            result = run_chat("Spiegami FastAPI", config=fake_config)

            mock_client.assert_called_once_with(fake_config)
            instance.chat.assert_called_once()
            messages = instance.chat.call_args[0][0]
            assert len(messages) == 2
            assert messages[0] == {"role": "system", "content": _CHAT_SYSTEM_CONTENT}
            assert messages[1] == {"role": "user", "content": "Spiegami FastAPI"}
            assert result is fake_chat_result

    def test_loads_default_config_when_none(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """When ``config=None``, run_chat calls ``load_config()`` to obtain the
        configuration."""
        with (
            mock.patch("qwen_dev_tutor.tutor.load_config") as mock_load_config,
            mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client,
        ):
            mock_load_config.return_value = fake_config
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            result = run_chat("Ciao")

            mock_load_config.assert_called_once_with()
            mock_client.assert_called_once_with(fake_config)
            assert result is fake_chat_result

    def test_propagates_client_error(self, fake_config: AppConfig) -> None:
        """When ``client.chat()`` raises, run_chat propagates the error
        unchanged."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.side_effect = QwenClientError("errore simulato")

            with pytest.raises(QwenClientError, match="errore simulato"):
                run_chat("test", config=fake_config)

    def test_strips_whitespace_from_prompt(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """Leading and trailing whitespace in the prompt is stripped before
        sending."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            run_chat("  \nCiao mondo  ", config=fake_config)

            messages = instance.chat.call_args[0][0]
            assert messages[1]["content"] == "Ciao mondo"


# ── run_code_tutor ────────────────────────────────────────────────────────────


class TestRunCodeTutor:
    """Tests for the synchronous ``run_code_tutor`` function."""

    def test_calls_client_chat_with_tutor_messages(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """run_code_tutor calls ``client.chat()`` with messages built by
        ``build_tutor_messages``."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            result = run_code_tutor("def f(): pass", config=fake_config)

            mock_client.assert_called_once_with(fake_config)
            instance.chat.assert_called_once()
            messages = instance.chat.call_args[0][0]
            assert len(messages) == 2
            assert messages[0]["role"] == "system"
            assert "developer tutor" in messages[0]["content"]
            assert "def f(): pass" in messages[1]["content"]
            assert "spiegalo in italiano" in messages[1]["content"]
            assert result is fake_chat_result

    def test_with_language_hint(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """When ``language_hint`` is provided, the hint line appears in the user
        message."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            run_code_tutor("x = 1", language_hint="python", config=fake_config)

            messages = instance.chat.call_args[0][0]
            assert "Linguaggio suggerito: python." in messages[1]["content"]

    def test_without_language_hint(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """When ``language_hint`` is None, no language line is included in the
        message."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            run_code_tutor("x = 1", config=fake_config)

            messages = instance.chat.call_args[0][0]
            assert "Linguaggio suggerito" not in messages[1]["content"]

    def test_loads_default_config_when_none(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """When ``config=None``, run_code_tutor falls back to ``load_config()``."""
        with (
            mock.patch("qwen_dev_tutor.tutor.load_config") as mock_load_config,
            mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client,
        ):
            mock_load_config.return_value = fake_config
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            result = run_code_tutor("x = 1")

            mock_load_config.assert_called_once_with()
            mock_client.assert_called_once_with(fake_config)
            assert result is fake_chat_result

    def test_propagates_client_error(self, fake_config: AppConfig) -> None:
        """When ``client.chat()`` raises, run_code_tutor propagates the error."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.side_effect = QwenClientError("errore codice")

            with pytest.raises(QwenClientError, match="errore codice"):
                run_code_tutor("x = 1", config=fake_config)

    def test_strips_whitespace_from_code_snippet(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """Leading and trailing whitespace in the code snippet is stripped."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.chat.return_value = fake_chat_result

            run_code_tutor("  \n\ndef f(): pass\n  ", config=fake_config)

            messages = instance.chat.call_args[0][0]
            assert "def f(): pass" in messages[1]["content"]
            # The entire user message should not have leading/trailing whitespace
            assert messages[1]["content"].strip() == messages[1]["content"]


# ── run_chat_async ────────────────────────────────────────────────────────────


class TestRunChatAsync:
    """Tests for the async ``run_chat_async`` function."""

    @pytest.mark.anyio
    async def test_calls_client_achat_with_chat_messages(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """run_chat_async calls ``client.achat()`` with the correct messages."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(return_value=fake_chat_result)

            result = await run_chat_async("Spiegami FastAPI", config=fake_config)

            mock_client.assert_called_once_with(fake_config)
            instance.achat.assert_awaited_once()
            messages = instance.achat.call_args[0][0]
            assert messages[1]["content"] == "Spiegami FastAPI"
            assert result is fake_chat_result

    @pytest.mark.anyio
    async def test_loads_default_config_when_none(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """When ``config=None``, run_chat_async calls ``load_config()``."""
        with (
            mock.patch("qwen_dev_tutor.tutor.load_config") as mock_load_config,
            mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client,
        ):
            mock_load_config.return_value = fake_config
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(return_value=fake_chat_result)

            result = await run_chat_async("Ciao")

            mock_load_config.assert_called_once_with()
            mock_client.assert_called_once_with(fake_config)
            assert result is fake_chat_result

    @pytest.mark.anyio
    async def test_propagates_client_error(self, fake_config: AppConfig) -> None:
        """When ``client.achat()`` raises, run_chat_async propagates the error."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(
                side_effect=QwenClientError("errore async"),
            )

            with pytest.raises(QwenClientError, match="errore async"):
                await run_chat_async("test", config=fake_config)


# ── run_code_tutor_async ──────────────────────────────────────────────────────


class TestRunCodeTutorAsync:
    """Tests for the async ``run_code_tutor_async`` function."""

    @pytest.mark.anyio
    async def test_calls_client_achat_with_tutor_messages(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """run_code_tutor_async calls ``client.achat()`` with tutor messages."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(return_value=fake_chat_result)

            result = await run_code_tutor_async("def f(): pass", config=fake_config)

            mock_client.assert_called_once_with(fake_config)
            instance.achat.assert_awaited_once()
            messages = instance.achat.call_args[0][0]
            assert "def f(): pass" in messages[1]["content"]
            assert result is fake_chat_result

    @pytest.mark.anyio
    async def test_with_language_hint(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """language_hint is passed through in the async version."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(return_value=fake_chat_result)

            await run_code_tutor_async(
                "x = 1",
                language_hint="python",
                config=fake_config,
            )

            messages = instance.achat.call_args[0][0]
            assert "Linguaggio suggerito: python." in messages[1]["content"]

    @pytest.mark.anyio
    async def test_loads_default_config_when_none(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """When ``config=None``, run_code_tutor_async falls back to
        ``load_config()``."""
        with (
            mock.patch("qwen_dev_tutor.tutor.load_config") as mock_load_config,
            mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client,
        ):
            mock_load_config.return_value = fake_config
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(return_value=fake_chat_result)

            result = await run_code_tutor_async("x = 1")

            mock_load_config.assert_called_once_with()
            mock_client.assert_called_once_with(fake_config)
            assert result is fake_chat_result

    @pytest.mark.anyio
    async def test_propagates_client_error(self, fake_config: AppConfig) -> None:
        """When the async client raises, run_code_tutor_async propagates it."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(
                side_effect=QwenClientError("errore tutor async"),
            )

            with pytest.raises(QwenClientError, match="errore tutor async"):
                await run_code_tutor_async("x = 1", config=fake_config)


class TestRunVisionAsync:
    """Tests for ``run_vision_async``."""

    @pytest.mark.anyio
    async def test_calls_client_achat_with_vision_messages(
        self,
        fake_config: AppConfig,
        fake_chat_result: ChatResult,
    ) -> None:
        """run_vision_async calls ``client.achat()`` with vision messages."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(return_value=fake_chat_result)
            result = await run_vision_async(
                image_base64="iVBORw0KGgo=",
                prompt="Cosa vedi?",
                config=fake_config,
            )
        assert result is fake_chat_result

    @pytest.mark.anyio
    async def test_propagates_client_error(self, fake_config: AppConfig) -> None:
        """When client raises, run_vision_async propagates."""
        with mock.patch("qwen_dev_tutor.tutor.OpenAICompatibleClient") as mock_client:
            instance = mock_client.return_value
            instance.achat = mock.AsyncMock(
                side_effect=QwenClientError("vision error"),
            )
            with pytest.raises(QwenClientError, match="vision error"):
                await run_vision_async(
                    image_base64="iVBORw0KGgo=",
                    prompt="test",
                    config=fake_config,
                )
