from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


class ModelsConfigError(ValueError):
    """Raised when models config cannot be loaded or parsed."""


@dataclass(slots=True)
class ModelEntry:
    name: str
    provider: str
    description: str = ""
    api_key_env: str = "QWEN_API_KEY"
    base_url: str = ""
    model: str = ""
    allow_empty_api_key: bool = False
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ModelEntry:
        known = {"name", "provider", "description", "api_key_env",
                 "base_url", "model", "allow_empty_api_key"}
        extra = {k: v for k, v in data.items() if k not in known}
        return cls(
            name=data["name"],
            provider=data.get("provider", ""),
            description=data.get("description", ""),
            api_key_env=data.get("api_key_env", "QWEN_API_KEY"),
            base_url=data.get("base_url", ""),
            model=data.get("model", ""),
            allow_empty_api_key=bool(data.get("allow_empty_api_key", False)),
            extra=extra,
        )


DEFAULT_MODELS_PATH = Path(__file__).resolve().parent.parent.parent / "config" / "models.example.yaml"


def load_models_config(path: str | Path | None = None) -> list[ModelEntry]:
    """Load model entries from a YAML file.

    Expected format:
        models:
          - name: qwen-hosted
            provider: alibaba-model-studio
            base_url: ...
            model: qwen-plus
    """
    if yaml is None:  # pragma: no cover
        raise ModelsConfigError(
            "PyYAML non installato. Esegui: pip install pyyaml"
        )

    target = Path(path) if path else DEFAULT_MODELS_PATH
    if not target.exists():
        raise ModelsConfigError(f"File configurazione modelli non trovato: {target}")

    raw = target.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if not isinstance(data, dict) or "models" not in data:
        raise ModelsConfigError(
            "Formato YAML non valido: manca la chiave 'models'."
        )

    models_list = data["models"]
    if not isinstance(models_list, list):
        raise ModelsConfigError("'models' deve essere una lista.")

    return [ModelEntry.from_dict(item) for item in models_list]


def resolve_config_from_entry(entry: ModelEntry) -> dict[str, str]:
    """Build an env-overrides dict from a ModelEntry."""
    from os import environ

    overrides: dict[str, str] = {
        "QWEN_PROVIDER": entry.provider,
        "QWEN_BASE_URL": entry.base_url,
        "QWEN_MODEL": entry.model,
    }
    if entry.api_key_env:
        key_val = environ.get(entry.api_key_env)
        if key_val:
            overrides["QWEN_API_KEY"] = key_val
    if entry.allow_empty_api_key:
        overrides["QWEN_ALLOW_EMPTY_API_KEY"] = "true"
    return overrides
