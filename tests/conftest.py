from __future__ import annotations

from unittest import mock

import pytest


@pytest.fixture(autouse=True)
def _prevent_dotenv_leak() -> None:
    """Impedisce che qualsiasi test carichi il .env di progetto in os.environ."""
    with mock.patch("qwen_dev_tutor.config._load_dotenv_file"):
        yield
