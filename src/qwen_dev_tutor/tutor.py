from __future__ import annotations

from .client import ChatResult, OpenAICompatibleClient
from .config import AppConfig, load_config
from .prompts import build_chat_messages, build_tutor_messages


def run_chat(prompt: str, config: AppConfig | None = None) -> ChatResult:
    effective_config = config or load_config()
    client = OpenAICompatibleClient(effective_config)
    return client.chat(build_chat_messages(prompt))


def run_code_tutor(
    code_snippet: str,
    language_hint: str | None = None,
    config: AppConfig | None = None,
) -> ChatResult:
    effective_config = config or load_config()
    client = OpenAICompatibleClient(effective_config)
    return client.chat(build_tutor_messages(code_snippet=code_snippet, language_hint=language_hint))


async def run_chat_async(prompt: str, config: AppConfig | None = None) -> ChatResult:
    effective_config = config or load_config()
    client = OpenAICompatibleClient(effective_config)
    return await client.achat(build_chat_messages(prompt))


async def run_code_tutor_async(
    code_snippet: str,
    language_hint: str | None = None,
    config: AppConfig | None = None,
) -> ChatResult:
    effective_config = config or load_config()
    client = OpenAICompatibleClient(effective_config)
    return await client.achat(
        build_tutor_messages(code_snippet=code_snippet, language_hint=language_hint)
    )

