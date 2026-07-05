from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from typing import Any

import httpx

from .config import AppConfig


class QwenClientError(RuntimeError):
    """Raised when the OpenAI-compatible endpoint cannot be used safely."""


@dataclass(slots=True)
class ChatResult:
    content: str
    model: str
    provider: str
    raw_response: dict[str, Any]


class OpenAICompatibleClient:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        return headers

    def _payload_stream(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        return self._payload(messages=messages, temperature=temperature) | {"stream": True}

    def _payload(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        return {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature,
        }

    def _extract_result(self, data: dict[str, Any]) -> ChatResult:
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise QwenClientError("Risposta del modello non valida.") from exc

        if not isinstance(content, str) or not content.strip():
            raise QwenClientError("Il contenuto della risposta del modello e' vuoto o non valido.")

        model = data.get("model") or self.config.model
        return ChatResult(
            content=content.strip(),
            model=str(model),
            provider=self.config.provider,
            raw_response=data,
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> ChatResult:
        try:
            with httpx.Client(timeout=self.config.timeout_seconds) as client:
                response = client.post(
                    self.config.chat_completions_url,
                    headers=self._headers(),
                    json=self._payload(messages=messages, temperature=temperature),
                )
                response.raise_for_status()
        except httpx.ConnectError as exc:
            raise QwenClientError("Endpoint Qwen non raggiungibile.") from exc
        except httpx.TimeoutException as exc:
            raise QwenClientError("Richiesta a Qwen scaduta per timeout.") from exc
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text.strip() or exc.response.reason_phrase
            raise QwenClientError(f"Errore HTTP dal provider: {detail}") from exc
        except httpx.RequestError as exc:
            raise QwenClientError(f"Errore di rete verso il provider: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise QwenClientError("Il provider ha restituito una risposta non JSON.") from exc

        return self._extract_result(payload)

    async def achat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> ChatResult:
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                response = await client.post(
                    self.config.chat_completions_url,
                    headers=self._headers(),
                    json=self._payload(messages=messages, temperature=temperature),
                )
                response.raise_for_status()
        except httpx.ConnectError as exc:
            raise QwenClientError("Endpoint Qwen non raggiungibile.") from exc
        except httpx.TimeoutException as exc:
            raise QwenClientError("Richiesta a Qwen scaduta per timeout.") from exc
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text.strip() or exc.response.reason_phrase
            raise QwenClientError(f"Errore HTTP dal provider: {detail}") from exc
        except httpx.RequestError as exc:
            raise QwenClientError(f"Errore di rete verso il provider: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise QwenClientError("Il provider ha restituito una risposta non JSON.") from exc

        return self._extract_result(payload)
    async def chat_stream_async(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> AsyncGenerator[str, None]:
        """Stream tokens from the chat completion endpoint (SSE)."""
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                async with client.stream(
                    "POST",
                    self.config.chat_completions_url,
                    headers=self._headers(),
                    json=self._payload_stream(messages=messages, temperature=temperature),
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data.strip() == "[DONE]":
                                return
                            try:
                                chunk = json.loads(data)
                                delta = chunk["choices"][0]["delta"].get("content", "")
                                if delta:
                                    yield delta
                            except (KeyError, IndexError, json.JSONDecodeError):
                                continue
        except httpx.ConnectError as exc:
            raise QwenClientError("Endpoint Qwen non raggiungibile.") from exc
        except httpx.TimeoutException as exc:
            raise QwenClientError("Richiesta a Qwen scaduta per timeout.") from exc
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text.strip() or exc.response.reason_phrase
            raise QwenClientError(f"Errore HTTP dal provider: {detail}") from exc
        except httpx.RequestError as exc:
            raise QwenClientError(f"Errore di rete verso il provider: {exc}") from exc
