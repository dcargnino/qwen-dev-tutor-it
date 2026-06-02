from __future__ import annotations

import pytest

from qwen_dev_tutor.config import AppConfig, ConfigError, get_config_issues, load_config


def test_load_config_success() -> None:
    config = load_config(
        overrides={
            "QWEN_PROVIDER": "test-provider",
            "QWEN_API_KEY": "abc123",
            "QWEN_BASE_URL": "http://localhost:11434",
            "QWEN_MODEL": "qwen-test",
            "QWEN_TIMEOUT_SECONDS": "15",
        }
    )

    assert isinstance(config, AppConfig)
    assert config.provider == "test-provider"
    assert config.model == "qwen-test"
    assert config.chat_completions_url == "http://localhost:11434/v1/chat/completions"


def test_load_config_requires_model() -> None:
    with pytest.raises(ConfigError):
        load_config(
            overrides={
                "QWEN_API_KEY": "abc123",
                "QWEN_BASE_URL": "http://localhost:11434",
            }
        )


def test_get_config_issues_allows_empty_api_key_for_local() -> None:
    issues = get_config_issues(
        overrides={
            "QWEN_ALLOW_EMPTY_API_KEY": "true",
            "QWEN_BASE_URL": "http://localhost:11434",
            "QWEN_MODEL": "qwen-local",
        }
    )

    assert issues == []

