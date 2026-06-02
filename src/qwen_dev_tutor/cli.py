from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .client import QwenClientError
from .config import ConfigError, load_config
from .tutor import run_chat, run_code_tutor


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qwen-dev-tutor",
        description="CLI minimale per testare Qwen in modalita' chat e developer tutor.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="Invia un prompt testuale a Qwen.")
    chat_parser.add_argument("prompt", help="Prompt utente da inviare al modello.")

    tutor_parser = subparsers.add_parser(
        "code-review",
        help="Analizza un file di codice con il developer tutor.",
    )
    tutor_parser.add_argument("path", help="Percorso del file da analizzare.")
    tutor_parser.add_argument(
        "--language",
        dest="language_hint",
        help="Hint opzionale sul linguaggio del file.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        config = load_config()
        if args.command == "chat":
            result = run_chat(args.prompt, config=config)
        else:
            code_path = Path(args.path)
            if not code_path.exists():
                raise FileNotFoundError(f"File non trovato: {code_path}")
            result = run_code_tutor(
                code_path.read_text(encoding="utf-8"),
                language_hint=args.language_hint,
                config=config,
            )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except ConfigError as exc:
        print(f"Errore configurazione: {exc}", file=sys.stderr)
        return 2
    except QwenClientError as exc:
        print(f"Errore client: {exc}", file=sys.stderr)
        return 3

    print(f"Provider: {result.provider}")
    print(f"Model: {result.model}")
    print()
    print(result.content)
    return 0

