<div align="center">

# Qwen Dev Tutor IT

[![Python](https://img.shields.io/badge/python-3.11%20|%203.12%20|%203.13-blue?logo=python)](https://python.org)
[![Tests](https://img.shields.io/badge/测试-104%20通过-green?logo=pytest)](https://github.com/dcargnino/qwen-dev-tutor-it/actions)
[![Ruff](https://img.shields.io/badge/ruff-0%20错误-brightgreen?logo=ruff)](https://github.com/astral-sh/ruff)
[![许可证](https://img.shields.io/badge/许可证-MIT-blue)](LICENSE)
[![最后提交](https://img.shields.io/github/last-commit/dcargnino/qwen-dev-tutor-it)](https://github.com/dcargnino/qwen-dev-tutor-it/commits/main)
[![欢迎 PR](https://img.shields.io/badge/PR-欢迎-brightgreen)](.github/pull_request_template.md)

> **将 Qwen 引入意大利开发者教育** — 一个为工作坊、社区聚会和技术分享设计的实用开源 MVP。

</div>

![Qwen model offering](assets/Qwen3.7-Max-June22.png)

 — 一个为工作坊、社区聚会和技术分享设计的实用开源 MVP。



---

## 为什么这个项目很重要

许多 AI 项目只展示模型"能回答"。这个项目展示更有趣的东西：

**如何以开发者优先的方式呈现、教授和采用 Qwen。**

Qwen 不是单一模型 — 它是阿里巴巴云 Qwen 团队开发的 **AI 模型家族**，包括：

- **通用 LLM**：聊天、推理、写作
- **编程模型**：代码解释、生成和审查
- **多模态模型**（视觉、音频）：更丰富的交互
- **API 托管版本**和**开源版本**

Qwen Dev Tutor IT 旨在搭建模型与实际使用者之间的**桥梁**——面向开发者、教育工作者、社区建设者和创客。

---

## 功能特性

| 领域 | 功能 |
|---|---|
| 💬 **文本聊天** | 用意大利语与 Qwen 交互问答 |
| 🧑‍💻 **开发者导师** | 粘贴代码 → 获得解释、改进建议和单元测试 |
| 👁️ **视觉分析器** | 上传图片 → Qwen 描述和分析 |
| 📊 **模型对比** | 在相同提示下并排比较多个 Qwen 模型 |
| 🖥️ **命令行** | `chat`、`code-review`、`compare` 命令 |
| 🌐 **API** | FastAPI 提供 `/chat`、`/tutor`、`/vision`、`/chat/stream` 端点 |
| 🎨 **网页界面** | 支持 SSE 流式传输、深色模式和复制功能的丰富界面 |
| 🔌 **提供商无关** | 兼容任何 OpenAI 兼容端点（托管或本地） |
| 🐳 **Docker** | 即用型 Dockerfile + docker-compose |

---

## 快速开始

### 前置条件

- Python 3.11+
- OpenAI 兼容端点（阿里云百炼、Ollama、vLLM、LM Studio...）

### 安装

```bash
# 克隆仓库
git clone https://github.com/dcargnino/qwen-dev-tutor-it.git
cd qwen-dev-tutor-it

# 创建虚拟环境并安装
uv venv --python 3.12
uv pip install -e ".[dev]"

# 配置端点
cp .env.example .env
# 编辑 .env 文件，填入 API key、base URL 和模型名称
```

### 配置

创建 `.env` 文件：

```env
QWEN_PROVIDER=alibaba-model-studio
QWEN_API_KEY=your-api-key-here
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode
QWEN_MODEL=qwen3.6-flash
QWEN_TIMEOUT_SECONDS=60
QWEN_ALLOW_EMPTY_API_KEY=false
```

本地部署（Ollama、vLLM、LM Studio）：

```env
QWEN_PROVIDER=ollama-local
QWEN_API_KEY=local-demo-key
QWEN_BASE_URL=http://localhost:11434
QWEN_MODEL=qwen2.5-coder:7b
QWEN_ALLOW_EMPTY_API_KEY=true
```

---

## 使用方法

### 命令行

```bash
# 文本聊天
python -m qwen_dev_tutor chat "用意大利语解释 FastAPI"

# 代码审查
python -m qwen_dev_tutor code-review examples/simple_function.py

# 模型对比
python -m qwen_dev_tutor compare "什么是 FastAPI？" --models qwen3.6-flash,qwen3-coder-flash

# 从 YAML 配置对比
python -m qwen_dev_tutor compare "解释 Python 装饰器" --from-yaml config/models.example.yaml
```

### API 服务器

```bash
uvicorn qwen_dev_tutor.api:app --reload --host 0.0.0.0 --port 8000
```

| 端点 | 方法 | 描述 |
|---|---|---|
| `/health` | GET | 配置状态 |
| `/chat` | POST | 文本聊天 |
| `/chat/stream` | POST | SSE 流式聊天 |
| `/tutor` | POST | 代码分析 |
| `/vision` | POST | 图像分析（base64） |
| `/` | GET | 网页界面 |

### Docker

```bash
docker compose up -d
```

---

## 项目结构

```
qwen-dev-tutor-it/
  README.md              # 文档（英文）
  README.it.md           # 文档（意大利文）
  README.zh-cn.md        # 文档（中文）
  .env.example           # 环境变量模板
  pyproject.toml         # 项目配置 + 依赖
  Makefile               # 常用目标（test, lint, run, docker）
  Dockerfile             # 多阶段 Docker 构建
  docker-compose.yml     # 快速部署
  config/
    models.example.yaml  # 多模型 YAML 配置
  exercises/
    01_text_chat.md      # 文本聊天练习
    02_code_explanation.md    # 代码解释练习
    03_model_comparison.md    # 模型对比练习
    04_vision.md          # 视觉分析练习
    05_audio.md           # 音频转录练习
    06_agentic_workflow.md    # 代理工作流练习
  src/qwen_dev_tutor/
    config.py            # 运行时配置
    client.py            # OpenAI 兼容 HTTP 客户端
    prompts.py           # 系统提示和消息构建器
    tutor.py             # 业务逻辑（聊天、导师、视觉）
    models.py            # 多模型 YAML 加载器
    api.py               # FastAPI 应用 + 网页界面
    cli.py               # CLI 入口
  tests/
    test_config.py       # 13 个测试
    test_client.py       # 22 个测试
    test_prompts.py      # 4 个测试
    test_tutor.py        # 22 个测试
    test_cli.py          # 15 个测试
    test_api.py          # 22 个测试
    test_models.py       # 9 个测试
```

---

## 练习

`exercises/` 文件夹包含完整的学习路径：

1. **文本聊天** — 与 Qwen 的基础交互
2. **代码解释** — 开发者导师工作流
3. **模型对比** — 比较不同 Qwen 模型
4. **视觉分析器** — 多模态图像分析
5. **音频与语音** — 转录和分析（STT + Qwen）
6. **代理工作流** — 仓库分析和问题生成

---

## 架构

```text
                         +----------------------+
                         |       用户           |
                         | 开发者 / 导师 / 创客 |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                                             |
             v                                             v
   +---------------------+                      +---------------------+
   | 网页界面             |                      | 命令行              |
   | 聊天 / 导师 /        |                      | 聊天 / 代码审查     |
   | 视觉（SSE 流）       |                      | 模型对比            |
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
                 | OpenAI 兼容 /v1/chat/...          |
                 +----------------+------------------+
                                  |
          +-----------------------+------------------------+
          |                        |                       |
          v                        v                       v
+------------------+   +---------------------+   +--------------------+
| 阿里云百炼       |   | Ollama / vLLM /     |   | 其他兼容端点      |
|（托管）          |   | LM Studio（本地）    |   |                    |
+------------------+   +---------------------+   +--------------------+
```

---

## 路线图

```text
今天
  |-- 意大利语文本聊天
  |-- 开发者导师（代码 → 解释 + 测试）
  |-- 视觉分析器
  |-- 命令行 + API + 网页界面
  |-- 模型对比
  |-- Docker + CI
  v
明天
  |-- 流式传输改进（导师 + 视觉 SSE）
  |-- 基准测试指标
  |-- 工作坊工具包
  |-- 社区活动材料
```

---

## 适用人群

- **开发者**：希望在真实编程任务中试用 Qwen
- **教育工作者和工作坊组织者**：需要实操材料
- **社区建设者和布道师**：围绕 Qwen 构建内容
- **创客和实验者**：探索模型对比

---

## 开发

```bash
# 运行测试
make test          # 或：.venv/bin/python -m pytest tests/ -v

# 代码检查
make lint          # 或：.venv/bin/ruff check src/qwen_dev_tutor/ tests/

# 格式化
make lint-fix

# 本地运行
make run
```

---

## 许可证

MIT — 详见 [LICENSE](LICENSE) 文件。
