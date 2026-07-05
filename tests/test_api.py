from __future__ import annotations

from unittest import mock

from fastapi.testclient import TestClient

from qwen_dev_tutor.api import create_app
from qwen_dev_tutor.client import ChatResult, QwenClientError
from qwen_dev_tutor.config import ConfigError


class TestHealth:
    """GET /health — reports configuration status."""

    def test_configured(self) -> None:
        issues: list[str] = []
        with mock.patch("qwen_dev_tutor.api.get_config_issues", return_value=issues):
            client = TestClient(create_app())
            resp = client.get("/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["configured"] is True
        assert data["issues"] == []

    def test_unconfigured(self) -> None:
        issues = [
            "QWEN_BASE_URL non configurata.",
            "QWEN_MODEL non configurato.",
        ]
        with mock.patch("qwen_dev_tutor.api.get_config_issues", return_value=issues):
            client = TestClient(create_app())
            resp = client.get("/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "needs_configuration"
        assert data["configured"] is False
        assert data["issues"] == issues


class TestChat:
    """POST /chat — text prompt to the model."""

    def test_success(self) -> None:
        mock_config = mock.MagicMock()
        mock_result = mock.MagicMock(spec=ChatResult)
        mock_result.provider = "test-provider"
        mock_result.model = "qwen-test"
        mock_result.content = "Ecco la spiegazione di FastAPI."

        with (
            mock.patch("qwen_dev_tutor.api.load_config", return_value=mock_config),
            mock.patch(
                "qwen_dev_tutor.api.run_chat_async", return_value=mock_result
            ),
        ):
            client = TestClient(create_app())
            resp = client.post(
                "/chat", json={"prompt": "Ciao, spiegami FastAPI."}
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["provider"] == "test-provider"
        assert data["model"] == "qwen-test"
        assert data["response"] == "Ecco la spiegazione di FastAPI."

    def test_empty_prompt_returns_422(self) -> None:
        client = TestClient(create_app())
        resp = client.post("/chat", json={"prompt": ""})

        assert resp.status_code == 422

    def test_config_error_returns_400(self) -> None:
        with mock.patch(
            "qwen_dev_tutor.api.load_config",
            side_effect=ConfigError("QWEN_BASE_URL mancante."),
        ):
            client = TestClient(create_app())
            resp = client.post("/chat", json={"prompt": "Ciao"})

        assert resp.status_code == 400
        assert resp.json()["detail"] == "QWEN_BASE_URL mancante."

    def test_client_error_returns_502(self) -> None:
        mock_config = mock.MagicMock()
        with (
            mock.patch(
                "qwen_dev_tutor.api.load_config", return_value=mock_config
            ),
            mock.patch(
                "qwen_dev_tutor.api.run_chat_async",
                side_effect=QwenClientError(
                    "Endpoint Qwen non raggiungibile."
                ),
            ),
        ):
            client = TestClient(create_app())
            resp = client.post("/chat", json={"prompt": "Ciao"})

        assert resp.status_code == 502
        assert "non raggiungibile" in resp.json()["detail"]


class TestTutor:
    """POST /tutor — code analysis via the developer tutor."""

    def test_success(self) -> None:
        mock_config = mock.MagicMock()
        mock_result = mock.MagicMock(spec=ChatResult)
        mock_result.provider = "test-provider"
        mock_result.model = "qwen-test"
        mock_result.content = "Analisi del codice."

        with (
            mock.patch(
                "qwen_dev_tutor.api.load_config", return_value=mock_config
            ),
            mock.patch(
                "qwen_dev_tutor.api.run_code_tutor_async",
                return_value=mock_result,
            ),
        ):
            client = TestClient(create_app())
            resp = client.post(
                "/tutor",
                json={"code": "def add(a, b): return a + b"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["provider"] == "test-provider"
        assert data["model"] == "qwen-test"
        assert data["response"] == "Analisi del codice."

    def test_with_language_hint(self) -> None:
        mock_config = mock.MagicMock()
        mock_result = mock.MagicMock(spec=ChatResult)
        mock_result.provider = "test-provider"
        mock_result.model = "qwen-test"
        mock_result.content = "Analisi Python."

        with (
            mock.patch(
                "qwen_dev_tutor.api.load_config", return_value=mock_config
            ),
            mock.patch(
                "qwen_dev_tutor.api.run_code_tutor_async",
                return_value=mock_result,
            ) as mock_tutor,
        ):
            client = TestClient(create_app())
            resp = client.post(
                "/tutor",
                json={"code": "x = 1", "language_hint": "python"},
            )

        assert resp.status_code == 200
        mock_tutor.assert_called_once_with(
            "x = 1", language_hint="python", config=mock_config
        )

    def test_empty_code_returns_422(self) -> None:
        client = TestClient(create_app())
        resp = client.post("/tutor", json={"code": ""})

        assert resp.status_code == 422

    def test_config_error_returns_400(self) -> None:
        with mock.patch(
            "qwen_dev_tutor.api.load_config",
            side_effect=ConfigError("QWEN_MODEL non configurato."),
        ):
            client = TestClient(create_app())
            resp = client.post(
                "/tutor",
                json={"code": "def add(a, b): return a + b"},
            )

        assert resp.status_code == 400
        assert resp.json()["detail"] == "QWEN_MODEL non configurato."

    def test_client_error_returns_502(self) -> None:
        mock_config = mock.MagicMock()
        with (
            mock.patch(
                "qwen_dev_tutor.api.load_config", return_value=mock_config
            ),
            mock.patch(
                "qwen_dev_tutor.api.run_code_tutor_async",
                side_effect=QwenClientError(
                    "Errore HTTP dal provider: 401"
                ),
            ),
        ):
            client = TestClient(create_app())
            resp = client.post(
                "/tutor",
                json={"code": "def add(a, b): return a + b"},
            )

        assert resp.status_code == 502
        assert "Errore HTTP" in resp.json()["detail"]


class TestIndex:
    """GET / — landing page HTML."""

    def test_contains_title(self) -> None:
        client = TestClient(create_app())
        resp = client.get("/")

        assert resp.status_code == 200
        assert resp.headers["content-type"] == "text/html; charset=utf-8"
        assert "Qwen Dev Tutor IT" in resp.text
        assert "<h1>Qwen Dev Tutor IT</h1>" in resp.text
