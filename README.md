<div align="center">

# Qwen Dev Tutor IT

[![Python](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-blue?logo=python)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-104%20passed-green?logo=pytest)](https://github.com/dcargnino/qwen-dev-tutor-it/actions)
[![Ruff](https://img.shields.io/badge/ruff-0%20errors-brightgreen?logo=ruff)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/dcargnino/qwen-dev-tutor-it)](https://github.com/dcargnino/qwen-dev-tutor-it/commits/main)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](.github/pull_request_template.md)

> **Bring Qwen into Italian developer education** — a practical, open-source MVP for workshops, community meetups, and technical storytelling.

</div>

![Qwen model offering](assets/Qwen3.7-Max-June22.png)

 — a practical, open-source MVP for workshops, community meetups, and technical storytelling.




[🇮🇹 Italiano](README.it.md) · [🇨🇳 中文](README.zh-cn.md)

---

## Why This Project Matters

Many AI projects show that a model "can answer." This project shows something more interesting:

**how Qwen can be presented, taught, and adopted in a developer-first context.**

Qwen is not a single model — it's a **family of AI models** from Alibaba Cloud's Qwen team, spanning:

- **General-purpose LLMs** for chat, reasoning, writing
- **Coding models** for explanation, generation, and review
- **Multimodal models** (vision, audio) for richer interactions
- **API-hosted** and **open-source** releases

Qwen Dev Tutor IT is designed to **bridge the gap** between models and the people who want to actually use them — developers, educators, community builders, and makers.

---

## Features

| Area | Capability |
|---|---|
| 💬 **Text Chat** | Interactive Q&A with Qwen in Italian |
| 🧑‍💻 **Developer Tutor** | Paste code → get explanation, improvements, and a unit test |
| 👁️ **Vision Analyzer** | Upload an image → Qwen describes and analyzes it |
| 📊 **Model Comparison** | Compare multiple Qwen models side-by-side on the same prompt |
| 🖥️ **CLI** | `chat`, `code-review`, `compare` commands |
| 🌐 **API** | FastAPI with `/chat`, `/tutor`, `/vision`, `/chat/stream` endpoints |
| 🎨 **Web UI** | Rich interface with SSE streaming, dark mode, and copy-to-clipboard |
| 🔌 **Provider-agnostic** | Works with any OpenAI-compatible endpoint (hosted or local) |
| 🐳 **Docker** | Ready-to-deploy Dockerfile + docker-compose |

---

## Quick Start

### Prerequisites

- Python 3.11+
- An OpenAI-compatible endpoint (Alibaba Model Studio, Ollama, vLLM, LM Studio...)

### Install

```bash
# Clone the repo
git clone https://github.com/dcargnino/qwen-dev-tutor-it.git
cd qwen-dev-tutor-it

# Create venv and install
uv venv --python 3.12
uv pip install -e ".[dev]"

# Configure your endpoint
cp .env.example .env
# Edit .env with your API key, base URL, and model
```

### Configuration

Create a `.env` file:

```env
QWEN_PROVIDER=alibaba-model-studio
QWEN_API_KEY=your-api-key-here
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode
QWEN_MODEL=qwen3.6-flash
QWEN_TIMEOUT_SECONDS=60
QWEN_ALLOW_EMPTY_API_KEY=false
```

For local setups (Ollama, vLLM, LM Studio):

```env
QWEN_PROVIDER=ollama-local
QWEN_API_KEY=local-demo-key
QWEN_BASE_URL=http://localhost:11434
QWEN_MODEL=qwen2.5-coder:7b
QWEN_ALLOW_EMPTY_API_KEY=true
```

---

## Usage

### CLI

```bash
# Text chat
python -m qwen_dev_tutor chat "Explain FastAPI in Italian"

# Code review
python -m qwen_dev_tutor code-review examples/simple_function.py

# Model comparison
python -m qwen_dev_tutor compare "What is FastAPI?" --models qwen3.6-flash,qwen3-coder-flash

# Compare from YAML config
python -m qwen_dev_tutor compare "Explain Python decorators" --from-yaml config/models.example.yaml
```

### API Server

```bash
uvicorn qwen_dev_tutor.api:app --reload --host 0.0.0.0 --port 8000
```

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Configuration status |
| `/chat` | POST | Text chat |
| `/chat/stream` | POST | SSE streaming chat |
| `/tutor` | POST | Code analysis |
| `/vision` | POST | Image analysis (base64) |
| `/` | GET | Web UI |

### Docker

```bash
docker compose up -d
```

---

## Project Structure

```
qwen-dev-tutor-it/
  README.md              # This file
  .env.example           # Environment template
  pyproject.toml         # Project config + dependencies
  Makefile               # Common targets (test, lint, run, docker)
  Dockerfile             # Multi-stage Docker build
  docker-compose.yml     # Quick deployment
  config/
    models.example.yaml  # Multi-model YAML configuration
  exercises/
    01_text_chat.md      # Text chat exercise
    02_code_explanation.md    # Code explanation exercise
    03_model_comparison.md    # Model comparison exercise
    04_vision.md          # Vision analysis exercise
    05_audio.md           # Audio transcription exercise
    06_agentic_workflow.md    # Agentic workflow exercise
  src/qwen_dev_tutor/
    config.py            # Runtime configuration
    client.py            # OpenAI-compatible HTTP client
    prompts.py           # System prompts and message builders
    tutor.py             # Business logic (chat, tutor, vision)
    models.py            # Multi-model YAML loader
    api.py               # FastAPI application + web UI
    cli.py               # CLI entry point
  tests/
    test_config.py       # 13 tests
    test_client.py       # 22 tests
    test_prompts.py      # 4 tests
    test_tutor.py        # 22 tests
    test_cli.py          # 15 tests
    test_api.py          # 22 tests
    test_models.py       # 9 tests
```

---

## Architecture

```text
                         +----------------------+
                         |       User           |
                         | dev / tutor / maker  |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                                             |
             v                                             v
   +---------------------+                      +---------------------+
   | Web UI              |                      | CLI                 |
   | chat / tutor /      |                      | chat / code-review  |
   | vision (SSE stream) |                      | compare             |
   +----------+----------+                      +----------+----------+
              \                                         /
               \                                       /
                v                                     v
                 +-----------------------------------+
                 | qwen_dev_tutor                    |
                 | config + prompts + client + tutor |
                 +----------------+------------------+
                                  |
                                  v
                 +-----------------------------------+
                 | OpenAI-compatible /v1/chat/...    |
                 +----------------+------------------+
                                  |
          +-----------------------+------------------------+
          |                        |                       |
          v                        v                       v
+------------------+   +---------------------+   +--------------------+
| Alibaba Model    |   | Ollama / vLLM /     |   | Other compatible   |
| Studio           |   | LM Studio (local)    |   | endpoints          |
+------------------+   +---------------------+   +--------------------+
```

---

## Exercises

The `exercises/` folder is the seed of a complete learning path:

1. **Text Chat** — basic interaction with Qwen
2. **Code Explanation** — developer tutor workflow
3. **Model Comparison** — compare different Qwen models
4. **Vision Analyzer** — multimodal image analysis
5. **Audio & Speech** — transcription and analysis (STT + Qwen)
6. **Agentic Workflow** — repo analysis and issue generation

---

## Roadmap

```text
Today
  |-- Text chat in Italian
  |-- Developer tutor (code → explanation + tests)
  |-- Vision analyzer
  |-- CLI + API + Web UI
  |-- Model comparison
  |-- Docker + CI
  v
Tomorrow
  |-- Streaming improvements (tutor + vision SSE)
  |-- Benchmark metrics
  |-- Workshop toolkit
  |-- Community sessions material
```

---

## Who Is This For

- **Developers** wanting to try Qwen on real coding tasks
- **Educators & workshop creators** needing hands-on material
- **Community builders & ambassadors** building around Qwen
- **Makers & experimenters** exploring model comparisons

---

## Development

```bash
# Run tests
make test          # or: .venv/bin/python -m pytest tests/ -v

# Lint
make lint          # or: .venv/bin/ruff check src/qwen_dev_tutor/ tests/

# Format
make lint-fix

# Run locally
make run
```

---

## License

MIT — see [LICENSE](LICENSE) for details.
