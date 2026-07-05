from __future__ import annotations

from unittest import mock

import httpx
import pytest

from qwen_dev_tutor.client import ChatResult, OpenAICompatibleClient, QwenClientError
from qwen_dev_tutor.config import AppConfig


@pytest.fixture
def config() -> AppConfig:
    return AppConfig(
        provider="test-provider",
        api_key="test-key",
        base_url="http://test:8000",
        model="qwen-test",
        timeout_seconds=10,
    )


@pytest.fixture
def client(config: AppConfig) -> OpenAICompatibleClient:
    return OpenAICompatibleClient(config)


class TestHeaders:
    def test_with_api_key(self, client: OpenAICompatibleClient) -> None:
        headers = client._headers()
        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"

    def test_without_api_key(self, config: AppConfig) -> None:
        config.api_key = None
        c = OpenAICompatibleClient(config)
        headers = c._headers()
        assert "Authorization" not in headers


class TestPayload:
    def test_default_temperature(self, client: OpenAICompatibleClient) -> None:
        payload = client._payload(messages=[{"role": "user", "content": "hi"}])
        assert payload["model"] == "qwen-test"
        assert payload["temperature"] == 0.2
        assert payload["messages"] == [{"role": "user", "content": "hi"}]

    def test_custom_temperature(self, client: OpenAICompatibleClient) -> None:
        payload = client._payload(messages=[{"role": "user", "content": "hi"}], temperature=0.8)
        assert payload["temperature"] == 0.8


class TestExtractResult:
    def test_success(self, client: OpenAICompatibleClient) -> None:
        data = {
            "choices": [{"message": {"content": "  ciao mondo  "}}],
            "model": "qwen-response",
        }
        result = client._extract_result(data)
        assert isinstance(result, ChatResult)
        assert result.content == "ciao mondo"
        assert result.model == "qwen-response"
        assert result.provider == "test-provider"

    def test_model_fallback_to_config(self, client: OpenAICompatibleClient) -> None:
        data = {
            "choices": [{"message": {"content": "hello"}}],
        }
        result = client._extract_result(data)
        assert result.model == "qwen-test"

    def test_missing_choices_key(self, client: OpenAICompatibleClient) -> None:
        with pytest.raises(QwenClientError, match="Risposta del modello non valida"):
            client._extract_result({})

    def test_empty_choices(self, client: OpenAICompatibleClient) -> None:
        with pytest.raises(QwenClientError, match="Risposta del modello non valida"):
            client._extract_result({"choices": []})

    def test_empty_content(self, client: OpenAICompatibleClient) -> None:
        with pytest.raises(QwenClientError, match="vuoto"):
            client._extract_result({"choices": [{"message": {"content": ""}}]})

    def test_whitespace_only_content(self, client: OpenAICompatibleClient) -> None:
        with pytest.raises(QwenClientError, match="vuoto"):
            client._extract_result({"choices": [{"message": {"content": "   "}}]})

    def test_none_content(self, client: OpenAICompatibleClient) -> None:
        with pytest.raises(QwenClientError, match="vuoto"):
            client._extract_result({"choices": [{"message": {"content": None}}]})


class TestChatSync:
    def test_success(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "Client") as mock_client:
            instance = mock_client.return_value.__enter__.return_value
            resp = mock.MagicMock()
            resp.status_code = 200
            resp.json.return_value = {"choices": [{"message": {"content": "risposta corretta"}}], "model": "qwen-test"}
            instance.post.return_value = resp
            result = client.chat([{"role": "user", "content": "test"}])
            assert result.content == "risposta corretta"
            assert result.model == "qwen-test"

    def test_connect_error(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "Client") as mock_client:
            instance = mock_client.return_value.__enter__.return_value
            instance.post.side_effect = httpx.ConnectError("connection refused")
            with pytest.raises(QwenClientError, match="non raggiungibile"):
                client.chat([{"role": "user", "content": "test"}])

    def test_timeout(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "Client") as mock_client:
            instance = mock_client.return_value.__enter__.return_value
            instance.post.side_effect = httpx.TimeoutException("timeout")
            with pytest.raises(QwenClientError, match="scaduta"):
                client.chat([{"role": "user", "content": "test"}])

    def test_http_error(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "Client") as mock_client:
            instance = mock_client.return_value.__enter__.return_value
            instance.post.side_effect = httpx.HTTPStatusError(
                "400 Bad Request",
                request=mock.MagicMock(),
                response=mock.MagicMock(status_code=400, text="Bad Request"),
            )
            with pytest.raises(QwenClientError, match="Errore HTTP"):
                client.chat([{"role": "user", "content": "test"}])

    def test_non_json_response(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "Client") as mock_client:
            instance = mock_client.return_value.__enter__.return_value
            resp = mock.MagicMock(status_code=200)
            resp.json.side_effect = ValueError("not json")
            instance.post.return_value = resp
            with pytest.raises(QwenClientError, match="non JSON"):
                client.chat([{"role": "user", "content": "test"}])

    def test_network_error(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "Client") as mock_client:
            instance = mock_client.return_value.__enter__.return_value
            instance.post.side_effect = httpx.RequestError("network broken")
            with pytest.raises(QwenClientError, match="di rete"):
                client.chat([{"role": "user", "content": "test"}])


class TestChatAsync:
    @pytest.mark.anyio
    async def test_success(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "AsyncClient") as mock_client:
            instance = mock_client.return_value.__aenter__.return_value
            resp = mock.AsyncMock()
            resp.status_code = 200
            resp.raise_for_status = mock.MagicMock()
            resp.json = mock.MagicMock(return_value={"choices": [{"message": {"content": "risposta async"}}], "model": "qwen-test"})
            instance.post = mock.AsyncMock(return_value=resp)
            result = await client.achat([{"role": "user", "content": "test"}])
            assert result.content == "risposta async"

    @pytest.mark.anyio
    async def test_connect_error(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "AsyncClient") as mock_client:
            instance = mock_client.return_value.__aenter__.return_value
            instance.post = mock.AsyncMock(side_effect=httpx.ConnectError("connection refused"))
            with pytest.raises(QwenClientError, match="non raggiungibile"):
                await client.achat([{"role": "user", "content": "test"}])

    @pytest.mark.anyio
    async def test_timeout(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "AsyncClient") as mock_client:
            instance = mock_client.return_value.__aenter__.return_value
            instance.post = mock.AsyncMock(side_effect=httpx.TimeoutException("timeout"))
            with pytest.raises(QwenClientError, match="scaduta"):
                await client.achat([{"role": "user", "content": "test"}])

    @pytest.mark.anyio
    async def test_http_error(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "AsyncClient") as mock_client:
            instance = mock_client.return_value.__aenter__.return_value
            instance.post = mock.AsyncMock(side_effect=httpx.HTTPStatusError(
                "400 Bad Request",
                request=mock.MagicMock(),
                response=mock.MagicMock(status_code=400, text="Bad Request"),
            ))
            with pytest.raises(QwenClientError, match="Errore HTTP"):
                await client.achat([{"role": "user", "content": "test"}])

    @pytest.mark.anyio
    async def test_non_json_response(self, client: OpenAICompatibleClient) -> None:
        with mock.patch.object(httpx, "AsyncClient") as mock_client:
            instance = mock_client.return_value.__aenter__.return_value
            resp = mock.AsyncMock()
            resp.status_code = 200
            resp.raise_for_status = mock.MagicMock()
            resp.json = mock.MagicMock(side_effect=ValueError("not json"))
            instance.post = mock.AsyncMock(return_value=resp)
            with pytest.raises(QwenClientError, match="non JSON"):
                await client.achat([{"role": "user", "content": "test"}])
