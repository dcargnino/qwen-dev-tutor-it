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


def test_build_vision_messages_uses_content_array() -> None:
    from qwen_dev_tutor.prompts import VISION_SYSTEM_PROMPT, build_vision_messages

    messages = build_vision_messages(
        image_base64="iVBORw0KGgo=",
        prompt="Cosa vedi?",
        media_type="image/png",
    )

    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == VISION_SYSTEM_PROMPT
    assert messages[1]["role"] == "user"
    assert isinstance(messages[1]["content"], list)
    assert messages[1]["content"][0]["type"] == "text"
    assert messages[1]["content"][0]["text"] == "Cosa vedi?"
    assert messages[1]["content"][1]["type"] == "image_url"
    assert "data:image/png;base64,iVBORw0KGgo=" in messages[1]["content"][1]["image_url"]["url"]


def test_build_vision_messages_strips_whitespace() -> None:
    from qwen_dev_tutor.prompts import build_vision_messages

    messages = build_vision_messages(
        image_base64="  iVBORw0KGgo=  ",
        prompt="  Descrivi  ",
    )
    assert messages[1]["content"][0]["text"] == "Descrivi"
    assert messages[1]["content"][1]["image_url"]["url"].count("base64,iVBORw0KGgo=") == 1
