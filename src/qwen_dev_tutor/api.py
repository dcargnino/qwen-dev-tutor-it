from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from .client import QwenClientError
from .config import ConfigError, get_config_issues, load_config
from .tutor import (
    run_chat_async,
    run_chat_stream_async,
    run_code_tutor_async,
    run_vision_async,
)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, description="Prompt testuale da inviare al modello.")


class TutorRequest(BaseModel):
    code: str = Field(min_length=1, description="Snippet di codice da analizzare.")
    language_hint: str | None = Field(default=None, description="Hint opzionale sul linguaggio.")


class VisionRequest(BaseModel):
    image_base64: str = Field(min_length=1, description="Immagine codificata in base64.")
    prompt: str = Field(min_length=1, description="Prompt per analizzare l'immagine.")
    media_type: str = Field(default="image/png", description="Tipo MIME dell'immagine.")


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

    @app.post("/chat/stream")
    async def chat_stream(request: ChatRequest):
        from fastapi.responses import StreamingResponse

        try:
            config = load_config()
        except ConfigError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        async def event_stream():
            try:
                async for token in run_chat_stream_async(request.prompt, config=config):
                    yield f"data: {token}\n\n"
                yield "data: [DONE]\n\n"
            except QwenClientError as exc:
                yield f"event: error\ndata: {exc}\n\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            },
        )

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

    @app.post("/vision")
    async def vision(request: VisionRequest) -> dict[str, str]:
        try:
            config = load_config()
            result = await run_vision_async(
                image_base64=request.image_base64,
                prompt=request.prompt,
                media_type=request.media_type,
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
        --bg: #f6f2e8; --panel: #fffdf8; --line: #d9cdb4;
        --ink: #1b1a17; --accent: #b9572f; --accent-dark: #7d3418;
        --spinner: #b9572f;
      }
      [data-theme="dark"] {
        --bg: #1a1814; --panel: #24211c; --line: #3d382f;
        --ink: #e8dfd0; --accent: #d97a50; --accent-dark: #b9572f;
        --spinner: #d97a50;
      }
      body { margin: 0; font-family: Georgia,"Times New Roman",serif;
        background: var(--bg); color: var(--ink); transition: background .3s,color .3s; }
      main { max-width: 960px; margin: 0 auto; padding: 32px 20px 56px; }
      h1,h2 { margin: 0 0 12px; }
      .hero { margin-bottom:24px; padding:24px; border:1px solid var(--line);
        background:var(--panel); box-shadow:0 18px 40px rgba(77,50,27,.08); }
      .grid { display:grid; gap:20px; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); }
      .card { padding:20px; background:var(--panel); border:1px solid var(--line); position:relative; }
      textarea,input,button { width:100%; box-sizing:border-box; font:inherit; }
      textarea,input { margin:12px 0; padding:12px; border:1px solid var(--line);
        background:var(--panel); color:var(--ink); }
      textarea { min-height:180px; resize:vertical; }
      button { margin-top:8px; padding:12px 14px; border:0;
        background:var(--accent); color:#fff; cursor:pointer; transition:background .2s; }
      button:hover { background:var(--accent-dark); }
      button:disabled { opacity:.5; cursor:not-allowed; }
      pre { white-space:pre-wrap; word-break:break-word; padding:14px;
        background:var(--panel); border:1px solid var(--line); position:relative; }
      .meta { font-size:.95rem; color:#5d5141; }
      .copy-btn { position:absolute; top:4px; right:4px; padding:4px 8px;
        font-size:.75rem; background:var(--line); color:var(--ink);
        border:none; cursor:pointer; border-radius:3px; }
      .spinner { display:inline-block; width:16px; height:16px;
        border:2px solid var(--line); border-top-color:var(--spinner);
        border-radius:50%; animation:spin .6s linear infinite;
        vertical-align:middle; margin-right:6px; }
      @keyframes spin { to { transform:rotate(360deg); } }
      .theme-toggle { position:fixed; top:12px; right:12px; padding:8px 12px;
        font-size:.85rem; background:var(--panel); border:1px solid var(--line);
        color:var(--ink); cursor:pointer; z-index:10; }
    </style>
  </head>
  <body>
    <button class="theme-toggle" onclick="toggleTheme()">\u263E Tema</button>
    <main>
      <section class="hero">
        <h1>Qwen Dev Tutor IT</h1>
        <p>MVP per testare Qwen in chat e developer tutoring, con endpoint OpenAI-compatible hosted o locali.</p>
        <p class="meta">Configura ".env", poi usa questa pagina per provare il modello.</p>
      </section>
      <section class="grid">
        <article class="card">
          <h2>Chat testuale <span style="font-size:.75rem;color:#888">(SSE)</span></h2>
          <input id="chatPrompt" value="Ciao, spiegami cos'e' FastAPI in italiano." />
          <button id="chatBtn" onclick="sendChatStream()">Invia prompt</button>
          <pre id="chatResult">Nessuna risposta ancora.<button class="copy-btn" onclick="copyResult('chatResult')">Copia</button></pre>
        </article>
        <article class="card">
          <h2>Developer Tutor</h2>
          <textarea id="codeInput">def add(a: int, b: int) -> int:
    return a + b</textarea>
          <input id="languageHint" value="python" />
          <button id="tutorBtn" onclick="sendTutor()">Analizza snippet</button>
          <pre id="tutorResult">Nessuna analisi ancora.<button class="copy-btn" onclick="copyResult('tutorResult')">Copia</button></pre>
        </article>
        <article class="card">
          <h2>Vision Analyzer</h2>
          <input type="file" id="imageInput" accept="image/*" onchange="previewImage(event)" />
          <img id="imagePreview" style="display:none;max-width:100%;margin:8px 0;border:1px solid var(--line);" />
          <input id="visionPrompt" value="Descrivi questa immagine in italiano." />
          <button id="visionBtn" onclick="sendVision()">Analizza immagine</button>
          <pre id="visionResult">Nessuna analisi ancora.<button class="copy-btn" onclick="copyResult('visionResult')">Copia</button></pre>
        </article>
      </section>
    </main>
    <script>
      function toggleTheme() {
        const html = document.documentElement;
        const cur = html.getAttribute("data-theme");
        html.setAttribute("data-theme", cur === "dark" ? "" : "dark");
        localStorage.setItem("qwen-theme", html.getAttribute("data-theme"));
      }
      if (localStorage.getItem("qwen-theme") === "dark")
        document.documentElement.setAttribute("data-theme", "dark");

      function copyResult(id) {
        const el = document.getElementById(id);
        const txt = el.textContent.replace("Copia","").trim();
        navigator.clipboard.writeText(txt).catch(function(){});
      }

      function setLoading(btnId, loading) {
        const btn = document.getElementById(btnId);
        btn.disabled = loading;
        btn.innerHTML = loading ? '<span class="spinner"></span>Caricamento...' : (btn.dataset.orig || btn.textContent);
      }

      async function sendChatStream() {
        const prompt = document.getElementById("chatPrompt").value;
        const target = document.getElementById("chatResult");
        const btn = document.getElementById("chatBtn");
        btn.dataset.orig = "Invia prompt";
        setLoading("chatBtn", true);
        target.textContent = "";

        try {
          const resp = await fetch("/chat/stream", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
          });
          if (!resp.ok) {
            const err = await resp.json();
            target.textContent = err.detail || "Errore sconosciuto.";
            setLoading("chatBtn", false);
            return;
          }
          const reader = resp.body.getReader();
          const decoder = new TextDecoder();
          let buffer = "";
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });
            const parts = buffer.split("\\n\\n");
            buffer = parts.pop() || "";
            for (const part of parts) {
              if (part.startsWith("data: ")) {
                const data = part.slice(6);
                if (data === "[DONE]") continue;
                target.textContent += data;
              }
            }
          }
        } catch (e) {
          target.textContent = "Errore di connessione: " + e.message;
        }
        setLoading("chatBtn", false);
      }

      async function sendTutor() {
        const code = document.getElementById("codeInput").value;
        const language_hint = document.getElementById("languageHint").value || null;
        const btn = document.getElementById("tutorBtn");
        btn.dataset.orig = "Analizza snippet";
        setLoading("tutorBtn", true);
        try {
          const resp = await fetch("/tutor", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, language_hint })
          });
          const payload = await resp.json();
          const target = document.getElementById("tutorResult");
          if (!resp.ok) { target.textContent = payload.detail || "Errore."; return; }
          target.textContent = "Provider: " + payload.provider + "\\nModel: " + payload.model + "\\n\\n" + payload.response;
        } finally { setLoading("tutorBtn", false); }
      }

      function previewImage(event) {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(e) {
          document.getElementById("imagePreview").src = e.target.result;
          document.getElementById("imagePreview").style.display = "block";
        };
        reader.readAsDataURL(file);
      }

      async function sendVision() {
        const file = document.getElementById("imageInput").files[0];
        if (!file) { alert("Seleziona un'immagine."); return; }
        const prompt = document.getElementById("visionPrompt").value;
        const btn = document.getElementById("visionBtn");
        btn.dataset.orig = "Analizza immagine";
        setLoading("visionBtn", true);
        try {
          const reader = new FileReader();
          reader.onload = async function(e) {
            const dataUrl = e.target.result;
            const comma = dataUrl.indexOf(",");
            const mediaType = dataUrl.substring(5, comma).split(";")[0];
            const base64 = dataUrl.substring(comma + 1);
            const resp = await fetch("/vision", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ image_base64: base64, prompt, media_type: mediaType })
            });
            const payload = await resp.json();
            const target = document.getElementById("visionResult");
            if (!resp.ok) { target.textContent = payload.detail || "Errore."; return; }
            target.textContent = "Provider: " + payload.provider + "\\nModel: " + payload.model + "\\n\\n" + payload.response;
          };
          reader.readAsDataURL(file);
        } finally { setLoading("visionBtn", false); }
      }
    </script>
  </body>
</html>
                """

    return app


app = create_app()

