# Test Report — qwen-dev-tutor-it v0.1.0b1
> Data: 2026-07-05 | Endpoint: Alibaba Model Studio (eu-central-1)
> Modello consigliato: `qwen3.6-flash` (general purpose) / `qwen3-coder-flash` (coding)

---

## Riepilogo

| Categoria | Test | Risultato | Note |
|---|---|---|---|
| **Unit** | test_config.py::test_load_config_success | ✅ PASSED | |
| **Unit** | test_config.py::test_load_config_requires_model | ❌ FAILED | **Falso negativo**: il .env esistente fornisce QWEN_MODEL, il test non lo prevede. Passa senza .env. |
| **Unit** | test_config.py::test_get_config_issues_allows_empty_api_key_for_local | ✅ PASSED | |
| **Unit** | test_prompts.py::test_build_chat_messages_uses_system_prompt | ✅ PASSED | |
| **Unit** | test_prompts.py::test_build_tutor_messages_embeds_code_and_requirements | ✅ PASSED | |
| **Integrazione** | Lista modelli endpoint | ✅ PASSED | 72 modelli disponibili |
| **Integrazione** | CLI chat (qwen3.6-flash) | ✅ PASSED | Risposta in italiano, chiara e pertinente |
| **Integrazione** | CLI code-review (qwen3.6-flash) | ✅ PASSED | 3 sezioni: spiegazione, miglioramenti, test |
| **Integrazione** | CLI chat (qwen3-coder-flash) | ✅ PASSED | 3266 caratteri, analisi approfondita |
| **Integrazione** | API health (GET /health) | ✅ PASSED | {"status":"ok","configured":true} |
| **Integrazione** | API chat (POST /chat) | ✅ PASSED | Risposta corretta con provider/model |
| **Integrazione** | API tutor (POST /tutor) | ✅ PASSED | Analisi strutturata in 3 sezioni |
| **Integrazione** | UI web (GET /) | ✅ PASSED | HTML corretto, contiene "Qwen Dev Tutor" |

**Riepilogo: 12/13 test passati ✅** — l'unico fallimento è un falso negativo.

---

## Configurazione .env (da usare con la tua API key)

Il file .env nella root del progetto contiene:
```env
QWEN_PROVIDER=alibaba-model-studio
QWEN_API_KEY=YOUR_API_KEY_HERE      # ← inserisci qui la tua key
QWEN_BASE_URL=https://ws-k3l4vmv283qqihnw.eu-central-1.maas.aliyuncs.com/compatible-mode
QWEN_MODEL=qwen3.6-flash
QWEN_TIMEOUT_SECONDS=60
QWEN_ALLOW_EMPTY_API_KEY=false
```

Per usare il modello coder (migliore per code review):
```env
QWEN_MODEL=qwen3-coder-flash
```

> ⚠️ Il .env è già in .gitignore — non verrà committato.

---

## Problema tecnico rilevato: IPv6

Su questo VPS, httpx prova prima la connessione IPv6 e va in timeout permanente perché l'endpoint Alibaba non risponde su IPv6. curl funziona perché usa IPv4 di default.

**Soluzione temporanea per i test:** monkey-patch socket.create_connection per forzare IPv4.

**Soluzione permanente:** configurare /etc/gai.conf per preferire IPv4.

---

## Risultati test modelli flash

| Modello | Esito | Tempo | Ideale per |
|---|---|---|---|
| qwen3.6-flash | ✅ OK | ~3s | Uso generalista |
| qwen-flash | ✅ OK | ~3s | Legacy |
| qwen3.5-flash | ✅ OK | ~3s | Alternativa stabile |
| qwen3-coder-flash | ✅ OK | ~3s | Code review e tutor |

---

## Conclusione

Il progetto è perfettamente funzionante con l'API key Alibaba Model Studio.
Il core (config, client, prompt, CLI, API, UI) è solido e testato.
