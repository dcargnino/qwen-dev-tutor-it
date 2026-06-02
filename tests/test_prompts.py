from __future__ import annotations

from qwen_dev_tutor.prompts import (
    CHAT_SYSTEM_PROMPT,
    TUTOR_SYSTEM_PROMPT,
    build_chat_messages,
    build_tutor_messages,
)


def test_build_chat_messages_uses_system_prompt() -> None:
    messages = build_chat_messages("Spiegami FastAPI")

    assert messages[0]["content"] == CHAT_SYSTEM_PROMPT
    assert messages[1]["content"] == "Spiegami FastAPI"


def test_build_tutor_messages_embeds_code_and_requirements() -> None:
    messages = build_tutor_messages("def add(a, b): return a + b", language_hint="python")
    user_message = messages[1]["content"]

    assert messages[0]["content"] == TUTOR_SYSTEM_PROMPT
    assert "Linguaggio suggerito: python." in user_message
    assert "spiegalo in italiano" in user_message
    assert "test unitario semplice" in user_message
    assert "def add(a, b): return a + b" in user_message
