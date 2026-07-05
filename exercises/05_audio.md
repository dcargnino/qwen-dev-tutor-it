# 05 - Audio & Speech

## Obiettivo

Esplorare l\'elaborazione audio con Qwen, concentrandosi su due scenari principali:
- **Trascrizione**: convertire audio in testo per documentazione tecnica
- **Analisi**: estrarre informazioni strutturate da spiegazioni vocali

## Prerequisiti

Per la trascrizione locale, installa una libreria di speech-to-text:

```bash
pip install faster-whisper
```

Oppure configura un endpoint audio-compatible (es. Qwen-Audio via API).

## Scenario 1: Trascrizione tecnica

Registra una breve spiegazione tecnica (30-60 secondi) e trascrivila:

```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("registrazione.wav", language="it")

testo_completo = " ".join(seg.text for seg in segments)
print(testo_completo)
```

## Scenario 2: Analisi della trascrizione

Invia il testo trascritto al modello Qwen per analisi strutturata:

```bash
# Usando la CLI chat
python -m qwen_dev_tutor chat "Riassumi questa spiegazione tecnica e
estrai i punti chiave: [testo_trascritto]"
```

Oppure via API:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analizza questa trascrizione:\n\n[testo]\n\nEstrai: 1) argomento principale, 2) punti chiave, 3) domande da approfondire"}'
```

## Cosa osservare

- La trascrizione e\' accurata? (italiano tecnico, acronimi, inglesismi)
- Qwen riesce a estrarre informazioni strutturate dal testo trascritto?
- Il workflow funziona per mini-lesson, standup tecnici o registrazioni di workshop?

## Estensioni future

- Integrazione diretta con API Qwen-Audio per analisi end-to-end
- Upload file audio via UI web
- Segmentazione temporale con timestamp
- Generazione automatica di appunti e follow-up checklist
