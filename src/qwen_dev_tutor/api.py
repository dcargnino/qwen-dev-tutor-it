from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .client import QwenClientError
from .config import ConfigError, get_config_issues, load_config
from .tutor import run_chat_async, run_code_tutor_async


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, description="Prompt testuale da inviare al modello.")


class TutorRequest(BaseModel):
    code: str = Field(min_length=1, description="Snippet di codice da analizzare.")
    language_hint: str | None = Field(default=None, description="Hint opzionale sul linguaggio.")


def create_app() -> FastAPI:
    app = FastAPI(
        title="Qwen Dev Tutor IT",
        description="MVP per provare Qwen in scenari di developer education.",
        version="0.1.0",
    )

    @app.get("/health")
    async def health() -> dict[str, object]:
        issues = get_config_issues()
        return {
            "status": "ok" if not issues else "needs_configuration",
            "configured": not issues,
            "issues": issues,
        }

    @app.post("/chat")
    async def chat(request: ChatRequest) -> dict[str, str]:
        try:
            config = load_config()
            result = await run_chat_async(request.prompt, config=config)
        except ConfigError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except QwenClientError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

        return {
            "provider": result.provider,
            "model": result.model,
            "response": result.content,
        }

    @app.post("/tutor")
    async def tutor(request: TutorRequest) -> dict[str, str]:
        try:
            config = load_config()
            result = await run_code_tutor_async(
                request.code,
                language_hint=request.language_hint,
                config=config,
            )
        except ConfigError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except QwenClientError as exc:
            raise HTTPException(status_code=502, detail=str(exc)) from exc

        return {
            "provider": result.provider,
            "model": result.model,
            "response": result.content,
        }

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return """
<!doctype html>
<html lang="it">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Qwen Dev Tutor IT</title>
    <style>
      :root {
        --bg: #f6f2e8;
        --panel: #fffdf8;
        --line: #d9cdb4;
        --ink: #1b1a17;
        --accent: #b9572f;
        --accent-dark: #7d3418;
      }
      body {
        margin: 0;
        font-family: Georgia, "Times New Roman", serif;
        background:
          radial-gradient(circle at top left, rgba(185, 87, 47, 0.15), transparent 30%),
          linear-gradient(180deg, #f8f3ea 0%, #efe5d3 100%);
        color: var(--ink);
      }
      main {
        max-width: 960px;
        margin: 0 auto;
        padding: 32px 20px 56px;
      }
      h1, h2 {
        margin: 0 0 12px;
      }
      .hero {
        margin-bottom: 24px;
        padding: 24px;
        border: 1px solid var(--line);
        background: rgba(255, 253, 248, 0.92);
        box-shadow: 0 18px 40px rgba(77, 50, 27, 0.08);
      }
      .grid {
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      }
      .card {
        padding: 20px;
        background: var(--panel);
        border: 1px solid var(--line);
        box-shadow: 0 14px 32px rgba(77, 50, 27, 0.06);
      }
      textarea, input, button {
        width: 100%;
        box-sizing: border-box;
        font: inherit;
      }
      textarea, input {
        margin: 12px 0;
        padding: 12px;
        border: 1px solid var(--line);
        background: #fffefb;
      }
      textarea {
        min-height: 180px;
        resize: vertical;
      }
      button {
        margin-top: 8px;
        padding: 12px 14px;
        border: 0;
        background: var(--accent);
        color: white;
        cursor: pointer;
      }
      button:hover {
        background: var(--accent-dark);
      }
      pre {
        white-space: pre-wrap;
        word-break: break-word;
        padding: 14px;
        background: #fffaf1;
        border: 1px solid var(--line);
      }
      .meta {
        font-size: 0.95rem;
        color: #5d5141;
      }
    </style>
  </head>
  <body>
    <main>
      <section class="hero">
        <h1>Qwen Dev Tutor IT</h1>
        <p>MVP per testare Qwen in modalita' chat e developer tutoring, con endpoint OpenAI-compatible hosted o locali.</p>
        <p class="meta">Configura `.env`, poi usa questa pagina per provare rapidamente il modello.</p>
      </section>
      <section class="grid">
        <article class="card">
          <h2>Chat testuale</h2>
          <input id="chatPrompt" value="Ciao, spiegami cos'e' FastAPI in italiano." />
          <button onclick="sendChat()">Invia prompt</button>
          <pre id="chatResult">Nessuna risposta ancora.</pre>
        </article>
        <article class="card">
          <h2>Developer Tutor</h2>
          <textarea id="codeInput">def add(a: int, b: int) -> int:
    return a + b</textarea>
          <input id="languageHint" value="python" />
          <button onclick="sendTutor()">Analizza snippet</button>
          <pre id="tutorResult">Nessuna analisi ancora.</pre>
        </article>
      </section>
    </main>
    <script>
      async function handleResponse(targetId, response) {
        const target = document.getElementById(targetId);
        const payload = await response.json();
        if (!response.ok) {
          target.textContent = payload.detail || "Errore sconosciuto.";
          return;
        }
        target.textContent =
          "Provider: " + payload.provider + "\\n" +
          "Model: " + payload.model + "\\n\\n" +
          payload.response;
      }

      async function sendChat() {
        const prompt = document.getElementById("chatPrompt").value;
        const response = await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt })
        });
        await handleResponse("chatResult", response);
      }

      async function sendTutor() {
        const code = document.getElementById("codeInput").value;
        const language_hint = document.getElementById("languageHint").value || null;
        const response = await fetch("/tutor", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code, language_hint })
        });
        await handleResponse("tutorResult", response);
      }
    </script>
  </body>
</html>
        """

    return app


app = create_app()

