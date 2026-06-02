from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from dotenv import load_dotenv


class ConfigError(ValueError):
    """Raised when required runtime configuration is missing or invalid."""


@dataclass(slots=True)
class AppConfig:
    provider: str
    api_key: str | None
    base_url: str
    model: str
    timeout_seconds: float = 60.0
    allow_empty_api_key: bool = False

    @property
    def chat_completions_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/v1/chat/completions"


def _to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _load_dotenv_file(env_file: str | Path | None = None) -> None:
    target = Path(env_file) if env_file is not None else Path.cwd() / ".env"
    if target.exists():
        load_dotenv(dotenv_path=target, override=False)


def _collect_env(overrides: Mapping[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ)
    if overrides:
        env.update(overrides)
    return env


def get_config_issues(
    overrides: Mapping[str, str] | None = None,
    env_file: str | Path | None = None,
) -> list[str]:
    _load_dotenv_file(env_file)
    env = _collect_env(overrides)

    issues: list[str] = []
    if not env.get("QWEN_BASE_URL"):
        issues.append("QWEN_BASE_URL non configurata.")
    if not env.get("QWEN_MODEL"):
        issues.append("QWEN_MODEL non configurato.")

    allow_empty_api_key = _to_bool(env.get("QWEN_ALLOW_EMPTY_API_KEY"))
    if not allow_empty_api_key and not env.get("QWEN_API_KEY"):
        issues.append("QWEN_API_KEY mancante.")

    return issues


def load_config(
    overrides: Mapping[str, str] | None = None,
    env_file: str | Path | None = None,
) -> AppConfig:
    issues = get_config_issues(overrides=overrides, env_file=env_file)
    if issues:
        raise ConfigError(" ".join(issues))

    env = _collect_env(overrides)
    timeout_raw = env.get("QWEN_TIMEOUT_SECONDS", "60")

    try:
        timeout_seconds = float(timeout_raw)
    except ValueError as exc:
        raise ConfigError("QWEN_TIMEOUT_SECONDS deve essere un numero.") from exc

    return AppConfig(
        provider=env.get("QWEN_PROVIDER", "openai-compatible"),
        api_key=env.get("QWEN_API_KEY"),
        base_url=env["QWEN_BASE_URL"],
        model=env["QWEN_MODEL"],
        timeout_seconds=timeout_seconds,
        allow_empty_api_key=_to_bool(env.get("QWEN_ALLOW_EMPTY_API_KEY")),
    )

