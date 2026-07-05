from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

from qwen_dev_tutor.cli import main
from qwen_dev_tutor.client import ChatResult, QwenClientError
from qwen_dev_tutor.config import ConfigError


@pytest.fixture
def mock_config() -> mock.MagicMock:
    return mock.MagicMock()


@pytest.fixture
def mock_chat_result() -> ChatResult:
    return ChatResult(
        content="test response",
        model="qwen-test",
        provider="test-provider",
        raw_response={},
    )


class TestChatSubcommand:
    def test_calls_run_chat(
        self,
        mock_config: mock.MagicMock,
        mock_chat_result: ChatResult,
    ) -> None:
        """chat subcommand calls run_chat with the prompt and config."""
        with (
            mock.patch("qwen_dev_tutor.cli.load_config", return_value=mock_config),
            mock.patch(
                "qwen_dev_tutor.cli.run_chat", return_value=mock_chat_result
            ) as mock_run_chat,
        ):
            exit_code = main(argv=["chat", "hello world"])

        assert exit_code == 0
        mock_run_chat.assert_called_once_with("hello world", config=mock_config)


class TestCodeReviewSubcommand:
    def test_reads_file_and_calls_run_code_tutor(
        self,
        tmp_path: Path,
        mock_config: mock.MagicMock,
        mock_chat_result: ChatResult,
    ) -> None:
        """code-review reads the file and calls run_code_tutor."""
        source = tmp_path / "hello.py"
        source.write_text("print('hello')", encoding="utf-8")

        with (
            mock.patch("qwen_dev_tutor.cli.load_config", return_value=mock_config),
            mock.patch(
                "qwen_dev_tutor.cli.run_code_tutor", return_value=mock_chat_result
            ) as mock_tutor,
        ):
            exit_code = main(argv=["code-review", str(source)])

        assert exit_code == 0
        mock_tutor.assert_called_once_with(
            "print('hello')",
            language_hint=None,
            config=mock_config,
        )

    def test_with_language_passthrough(
        self,
        tmp_path: Path,
        mock_config: mock.MagicMock,
        mock_chat_result: ChatResult,
    ) -> None:
        """--language hint is passed through to run_code_tutor."""
        source = tmp_path / "main.js"
        source.write_text("console.log('hi')", encoding="utf-8")

        with (
            mock.patch("qwen_dev_tutor.cli.load_config", return_value=mock_config),
            mock.patch(
                "qwen_dev_tutor.cli.run_code_tutor", return_value=mock_chat_result
            ) as mock_tutor,
        ):
            exit_code = main(
                argv=["code-review", str(source), "--language", "javascript"]
            )

        assert exit_code == 0
        mock_tutor.assert_called_once_with(
            "console.log('hi')",
            language_hint="javascript",
            config=mock_config,
        )

    def test_file_not_found_returns_1(
        self, mock_config: mock.MagicMock
    ) -> None:
        """Non-existent file path returns exit code 1."""
        with (
            mock.patch("qwen_dev_tutor.cli.load_config", return_value=mock_config),
            mock.patch("qwen_dev_tutor.cli.run_code_tutor") as mock_tutor,
        ):
            exit_code = main(
                argv=["code-review", "/nonexistent/path/to/file.py"]
            )

        assert exit_code == 1
        mock_tutor.assert_not_called()


class TestErrorHandling:
    def test_config_error_returns_2(self) -> None:
        """ConfigError during any subcommand returns exit code 2."""
        with mock.patch(
            "qwen_dev_tutor.cli.load_config",
            side_effect=ConfigError("QWEN_MODEL non configurato."),
        ):
            exit_code = main(argv=["chat", "hello"])

        assert exit_code == 2

    def test_qwen_client_error_on_chat_returns_3(
        self, mock_config: mock.MagicMock
    ) -> None:
        """QwenClientError from run_chat returns exit code 3."""
        with (
            mock.patch("qwen_dev_tutor.cli.load_config", return_value=mock_config),
            mock.patch(
                "qwen_dev_tutor.cli.run_chat",
                side_effect=QwenClientError("API error"),
            ),
        ):
            exit_code = main(argv=["chat", "hello"])

        assert exit_code == 3

    def test_qwen_client_error_on_code_review_returns_3(
        self,
        tmp_path: Path,
        mock_config: mock.MagicMock,
    ) -> None:
        """QwenClientError from run_code_tutor returns exit code 3."""
        source = tmp_path / "test.py"
        source.write_text("code", encoding="utf-8")

        with (
            mock.patch("qwen_dev_tutor.cli.load_config", return_value=mock_config),
            mock.patch(
                "qwen_dev_tutor.cli.run_code_tutor",
                side_effect=QwenClientError("API error"),
            ),
        ):
            exit_code = main(argv=["code-review", str(source)])

        assert exit_code == 3


class TestArgparseErrors:
    def test_no_subcommand_returns_2(self) -> None:
        """No subcommand triggers argparse error (SystemExit 2)."""
        with pytest.raises(SystemExit) as excinfo:
            main(argv=[])
        assert excinfo.value.code == 2

    def test_missing_required_argument_returns_2(self) -> None:
        """Missing required positional argument triggers SystemExit 2."""
        with pytest.raises(SystemExit) as excinfo:
            main(argv=["chat"])
        assert excinfo.value.code == 2
