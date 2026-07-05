#!/usr/bin/env bash
# Qwen Dev Tutor IT — Automated Demo Script
# Runs exercises 01-03 in sequence to demonstrate the project.
set -euo pipefail

cd "$(dirname "$0")/.."

echo "============================================"
echo "  Qwen Dev Tutor IT — Automated Demo"
echo "============================================"
echo ""

# Check .env
if ! grep -q "QWEN_API_KEY=" .env 2>/dev/null || grep -q "YOUR_API_KEY_HERE" .env 2>/dev/null; then
    echo "⚠️  .env not configured. Set QWEN_API_KEY before running."
    exit 1
fi

echo ">>> 1/3: Text Chat"
echo "---"
python -m qwen_dev_tutor chat "Ciao, spiegami cos'e' FastAPI in italiano in massimo 3 righe."
echo ""
echo "✅ Done"
echo ""

echo ">>> 2/3: Code Review"
echo "---"
python -m qwen_dev_tutor code-review examples/simple_function.py
echo ""
echo "✅ Done"
echo ""

echo ">>> 3/3: Model Comparison (qwen3.6-flash vs qwen3-coder-flash)"
echo "---"
python -m qwen_dev_tutor compare "Spiegami cos'e' FastAPI" \
    --models qwen3.6-flash,qwen3-coder-flash
echo ""
echo "✅ Done"
echo ""

echo "============================================"
echo "  Demo completed successfully! 🎉"
echo "============================================"
