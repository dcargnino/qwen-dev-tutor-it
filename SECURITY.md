# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅ Active development |

## Reporting a Vulnerability

This project handles API keys and environment variables. If you discover a security vulnerability:

1. **Do not** open a public GitHub issue.
2. Send details to the maintainer via a [private security advisory](https://github.com/dcargnino/qwen-dev-tutor-it/security/advisories/new).
3. Include:
   - Type of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

You should receive a response within 48 hours.

## Best Practices

- Never commit `.env` files (it's in `.gitignore`).
- Rotate API keys if accidentally exposed.
- Use `QWEN_ALLOW_EMPTY_API_KEY=true` only for local endpoints (Ollama, vLLM, LM Studio).
- Keep dependencies updated: `uv sync --upgrade`.
