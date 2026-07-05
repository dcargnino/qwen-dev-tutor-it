from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .client import QwenClientError
from .config import AppConfig, ConfigError, load_config
from .models import load_models_config, resolve_config_from_entry
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

    compare_parser = subparsers.add_parser(
        "compare",
        help="Confronta modelli Qwen sullo stesso prompt.",
    )
    compare_parser.add_argument("prompt", help="Prompt da inviare a tutti i modelli.")
    compare_parser.add_argument(
        "--models",
        default=None,
        help="Nomi dei modelli separati da virgola (es. qwen3.6-flash,qwen3-coder-flash).",
    )
    compare_parser.add_argument(
        "--from-yaml",
        default=None,
        help="Percorso file YAML con configurazione modelli (default: config/models.example.yaml).",
    )

    return parser



def _format_table(rows: list[list[str]]) -> str:
    """Render a simple aligned table."""
    if not rows:
        return ""
    col_widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    lines: list[str] = []
    for i, row in enumerate(rows):
        line = "  ".join(cell.ljust(w) for cell, w in zip(row, col_widths))
        lines.append(line)
        if i == 0:
            lines.append("  ".join("-" * w for w in col_widths))
    return "\n".join(lines)


def _run_compare(args: argparse.Namespace) -> int:
    import time as time_module

    # Collect model configurations
    model_configs: list[tuple[str, dict[str, str]]] = []

    if args.from_yaml:
        entries = load_models_config(args.from_yaml)
        for entry in entries:
            overrides = resolve_config_from_entry(entry)
            model_configs.append((entry.name, overrides))
    elif args.models:
        names = [m.strip() for m in args.models.split(",") if m.strip()]
        for name in names:
            model_configs.append((name, {}))
    else:
        print("Specifica --models o --from-yaml.", file=sys.stderr)
        return 1

    print(f"Confronto {len(model_configs)} modello/i sul prompt:")
    print(f"  \"{args.prompt}\"")
    print()

    results_table = [["Modello", "Provider", "Tempo (s)", "Lunghezza", "Anteprima"]]
    errors: list[str] = []
    first_config = load_config()

    for name, overrides in model_configs:
        cfg = first_config
        if overrides:
            cfg = AppConfig(
                provider=overrides.get("QWEN_PROVIDER", first_config.provider),
                api_key=overrides.get("QWEN_API_KEY", first_config.api_key),
                base_url=overrides.get("QWEN_BASE_URL", first_config.base_url),
                model=overrides.get("QWEN_MODEL", name),
                timeout_seconds=first_config.timeout_seconds,
                allow_empty_api_key=overrides.get("QWEN_ALLOW_EMPTY_API_KEY", "false").lower()
                in ("1", "true", "yes", "on"),
            )

        start = time_module.monotonic()
        try:
            result = run_chat(args.prompt, config=cfg)
            elapsed = time_module.monotonic() - start
            preview = result.content[:60].replace("\n", " ").strip()
            results_table.append([
                name,
                result.provider,
                f"{elapsed:.1f}",
                str(len(result.content)),
                preview,
            ])
        except (ConfigError, QwenClientError) as exc:
            elapsed = time_module.monotonic() - start
            errors.append(f"{name}: {exc} (dopo {elapsed:.1f}s)")
            results_table.append([name, "ERRORE", f"{elapsed:.1f}", "-", str(exc)[:60]])

    print(_format_table(results_table))
    print()

    if errors:
        print("Errori:")
        for err in errors:
            print(f"  - {err}")
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "compare":
            return _run_compare(args)
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

