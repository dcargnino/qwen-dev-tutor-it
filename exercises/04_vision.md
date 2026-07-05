# 04 - Vision Analyzer

## Obiettivo

Usare un modello Qwen multimodale (es. `qwen3-vl-flash`) per analizzare immagini:
- descrizione del contenuto;
- estrazione di informazioni utili;
- generazione di checklist operative.

## Prerequisiti

Assicurati che il modello configurato in `.env` supporti input multimodali.
Esempio:
```env
QWEN_MODEL=qwen3-vl-flash
QWEN_BASE_URL=https://ws-k3l4vmv283qqihnw.eu-central-1.maas.aliyuncs.com/compatible-mode
```

## Scenario d'uso possibile

Caricare uno screenshot di un'interfaccia o di un errore e chiedere:

```text
Descrivi l'immagine, individua gli elementi principali e suggerisci una checklist di debug.
```

## Come provarlo

### UI web

1. Avvia il server: `uvicorn qwen_dev_tutor.api:app`
2. Apri `http://localhost:8000`
3. Vai alla sezione **Vision Analyzer**
4. Carica un'immagine, inserisci un prompt, clicca "Analizza immagine"

### API diretta

```bash
# Converti immagine in base64 (Linux/macOS)
BASE64=$(base64 -w0 percorso/immagine.png)

curl -X POST http://localhost:8000/vision \
  -H "Content-Type: application/json" \
  -d '{"image_base64":"'$BASE64'","prompt":"Descrivi questa immagine","media_type":"image/png"}'
```

## Cosa osservare

- La descrizione e' accurata e pertinente?
- Il modello riconosce elementi visivi come testo, icone, diagrammi?
- La risposta e' utile per debugging, documentazione o review?
- Quanto tempo impiega il modello a rispondere?

## Estensioni possibili

- OCR su screenshot di codice o documenti
- UI review: chiedi al modello di valutare un'interfaccia utente
- Document parsing: estrai testo strutturato da diagrammi o slide
- Generazione di test case a partire da screenshot di feature
