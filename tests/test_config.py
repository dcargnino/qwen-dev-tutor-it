from __future__ import annotations

from unittest import mock

import pytest

from qwen_dev_tutor.config import AppConfig, ConfigError, get_config_issues, load_config


@pytest.fixture(autouse=True)
def _no_dotenv() -> None:
    """Impedisce il caricamento del .env di progetto."""
    with mock.patch("qwen_dev_tutor.config._load_dotenv_file"):
        yield


@pytest.fixture
def base_overrides() -> dict[str, str]:
    return {
        "QWEN_API_KEY": "abc123",
        "QWEN_BASE_URL": "http://localhost:11434",
        "QWEN_MODEL": "qwen-test",
    }


class TestLoadConfig:
    def test_success(self, base_overrides: dict[str, str]) -> None:
        overrides = {**base_overrides, "QWEN_PROVIDER": "test-provider", "QWEN_TIMEOUT_SECONDS": "15"}
        config = load_config(overrides=overrides)

        assert isinstance(config, AppConfig)
        assert config.provider == "test-provider"
        assert config.model == "qwen-test"
        assert config.chat_completions_url == "http://localhost:11434/v1/chat/completions"

    def test_requires_model(self, base_overrides: dict[str, str]) -> None:
        del base_overrides["QWEN_MODEL"]
        with pytest.raises(ConfigError, match="QWEN_MODEL"):
            load_config(overrides=base_overrides)

    def test_requires_base_url(self, base_overrides: dict[str, str]) -> None:
        del base_overrides["QWEN_BASE_URL"]
        with pytest.raises(ConfigError, match="QWEN_BASE_URL"):
            load_config(overrides=base_overrides)

    def test_invalid_timeout(self, base_overrides: dict[str, str]) -> None:
        overrides = {**base_overrides, "QWEN_TIMEOUT_SECONDS": "non-numerico"}
        with pytest.raises(ConfigError, match="deve essere un numero"):
            load_config(overrides=overrides)

    def test_default_timeout(self, base_overrides: dict[str, str]) -> None:
        config = load_config(overrides=base_overrides)
        assert config.timeout_seconds == 60.0

    def test_default_provider(self, base_overrides: dict[str, str]) -> None:
        config = load_config(overrides=base_overrides)
        assert config.provider == "openai-compatible"

    def test_chat_completions_url(self, base_overrides: dict[str, str]) -> None:
        overrides = {**base_overrides, "QWEN_BASE_URL": "https://example.com/api"}
        config = load_config(overrides=overrides)
        assert config.chat_completions_url == "https://example.com/api/v1/chat/completions"

    def test_chat_completions_url_trailing_slash(self, base_overrides: dict[str, str]) -> None:
        overrides = {**base_overrides, "QWEN_BASE_URL": "https://example.com/api/"}
        config = load_config(overrides=overrides)
        assert config.chat_completions_url == "https://example.com/api/v1/chat/completions"


class TestGetConfigIssues:
    def test_returns_all_missing(self) -> None:
        issues = get_config_issues(overrides={"QWEN_API_KEY": "abc123"})
        assert any("QWEN_BASE_URL" in i for i in issues)
        assert any("QWEN_MODEL" in i for i in issues)

    def test_allows_empty_api_key_for_local(self) -> None:
        issues = get_config_issues(
            overrides={
                "QWEN_ALLOW_EMPTY_API_KEY": "true",
                "QWEN_BASE_URL": "http://localhost:11434",
                "QWEN_MODEL": "qwen-local",
            }
        )
        assert issues == []

    def test_requires_api_key_when_not_allowed(self) -> None:
        issues = get_config_issues(
            overrides={
                "QWEN_BASE_URL": "http://localhost:11434",
                "QWEN_MODEL": "qwen-test",
            }
        )
        assert any("QWEN_API_KEY" in i for i in issues)

    def test_allow_empty_api_key_false_by_default(self) -> None:
        issues = get_config_issues(
            overrides={
                "QWEN_BASE_URL": "http://localhost:11434",
                "QWEN_MODEL": "qwen-test",
            }
        )
        assert any("QWEN_API_KEY" in i for i in issues)

    def test_allow_empty_api_key_explicit_false(self) -> None:
        issues = get_config_issues(
            overrides={
                "QWEN_ALLOW_EMPTY_API_KEY": "false",
                "QWEN_BASE_URL": "http://localhost:11434",
                "QWEN_MODEL": "qwen-test",
            }
        )
        assert any("QWEN_API_KEY" in i for i in issues)
