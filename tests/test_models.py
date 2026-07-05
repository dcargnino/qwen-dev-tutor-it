from __future__ import annotations

from pathlib import Path

import pytest

from qwen_dev_tutor.models import (
    DEFAULT_MODELS_PATH,
    ModelEntry,
    ModelsConfigError,
    load_models_config,
    resolve_config_from_entry,
)


class TestModelEntry:
    def test_from_dict_minimal(self) -> None:
        entry = ModelEntry.from_dict({"name": "test-model"})
        assert entry.name == "test-model"
        assert entry.provider == ""
        assert entry.allow_empty_api_key is False

    def test_from_dict_full(self) -> None:
        entry = ModelEntry.from_dict({
            "name": "qwen-hosted",
            "provider": "alibaba-model-studio",
            "description": "test desc",
            "api_key_env": "MY_KEY",
            "base_url": "https://example.com",
            "model": "qwen-test",
            "allow_empty_api_key": True,
        })
        assert entry.name == "qwen-hosted"
        assert entry.provider == "alibaba-model-studio"
        assert entry.base_url == "https://example.com"
        assert entry.model == "qwen-test"
        assert entry.allow_empty_api_key is True

    def test_from_dict_extra_fields(self) -> None:
        entry = ModelEntry.from_dict({
            "name": "m", "extra_field": "kept"
        })
        assert entry.extra == {"extra_field": "kept"}


class TestLoadModelsConfig:
    def test_loads_default_yaml(self) -> None:
        """The bundled config/models.example.yaml must parse correctly."""
        models = load_models_config(str(DEFAULT_MODELS_PATH))
        assert len(models) >= 5
        assert models[0].name == "qwen-hosted"

    def test_file_not_found(self) -> None:
        with pytest.raises(ModelsConfigError, match="non trovato"):
            load_models_config("/tmp/nonexistent.yaml")

    def test_missing_models_key(self, tmp_path: Path) -> None:
        f = tmp_path / "bad.yaml"
        f.write_text("not_models: []")
        with pytest.raises(ModelsConfigError, match="manca la chiave"):
            load_models_config(str(f))

    def test_models_not_a_list(self, tmp_path: Path) -> None:
        f = tmp_path / "bad.yaml"
        f.write_text("models: not-a-list")
        with pytest.raises(ModelsConfigError, match="deve essere una lista"):
            load_models_config(str(f))

    def test_parses_yaml_with_models(self, tmp_path: Path) -> None:
        f = tmp_path / "good.yaml"
        f.write_text("""
models:
  - name: m1
    provider: p1
    base_url: http://a
    model: qwen-a
  - name: m2
    provider: p2
    base_url: http://b
    model: qwen-b
""")
        models = load_models_config(str(f))
        assert len(models) == 2
        assert models[0].name == "m1"
        assert models[1].name == "m2"


class TestResolveConfigFromEntry:
    def test_basic_fields(self) -> None:
        entry = ModelEntry(
            name="test", provider="p", base_url="http://x",
            model="qwen-t", api_key_env="QWEN_API_KEY",
        )
        overrides = resolve_config_from_entry(entry)
        assert overrides["QWEN_PROVIDER"] == "p"
        assert overrides["QWEN_BASE_URL"] == "http://x"
        assert overrides["QWEN_MODEL"] == "qwen-t"

    def test_allow_empty_api_key(self) -> None:
        entry = ModelEntry(
            name="test", provider="p", base_url="http://x",
            model="qwen-t", allow_empty_api_key=True,
        )
        overrides = resolve_config_from_entry(entry)
        assert overrides["QWEN_ALLOW_EMPTY_API_KEY"] == "true"
