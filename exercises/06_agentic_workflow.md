# 06 - Agentic Workflow

## Obiettivo

Costruire un mini-workflow agentico in cui Qwen analizza un piccolo repository locale e produce:
1. Analisi della struttura del codice
2. Identificazione di aree poco testate o migliorabili
3. Proposta di issue, test o checklist operative

## Prerequisiti

- Un repository Python locale (es. questo stesso progetto)
- CLI configurata con un modello Qwen (es. \`qwen3-coder-flash\`)

## Workflow guidato

### Step 1: Panoramica del progetto

```bash
# Ottieni una vista d\'insieme del repository
find . -name "*.py" | head -20

# Conta file e righe
find . -name "*.py" | wc -l
find . -name "*.py" -exec wc -l {} + | tail -1
```

### Step 2: Analisi strutturale

Invia la struttura del progetto a Qwen per un\'analisi iniziale:

```bash
python -m qwen_dev_tutor chat "Analizza la struttura di questo
progetto Python:
$(find . -name "*.py" -path "*/src/*" | sort | while read f; do
  echo "- $f ($(wc -l < "$f") righe)"; done)

Obiettivi dell\'analisi:
1. Quali sono i moduli principali e le loro responsabilita\'?
2. Ci sono pattern architetturali evidenti?
3. Quali sono i punti di ingresso (CLI, API)?
4. Ci sono aree che sembrano poco coperte da test?"
```

### Step 3: Code review mirata

```bash
# Analizza un modulo specifico con il developer tutor
python -m qwen_dev_tutor code-review src/qwen_dev_tutor/client.py
```

### Step 4: Generazione issue

Invia a Qwen le osservazioni raccolte e chiedi un piano d\'azione:

```bash
python -m qwen_dev_tutor chat "Sulla base dell\'analisi del progetto,
genera 3-5 issue strutturate in formato markdown:
- Titolo
- Descrizione del problema/miglioramento
- Impatto (basso/medio/alto)
- Suggerimento per implementazione
- Test suggeriti"
```

## Output atteso

Uno o piu\' file markdown con:

- \`docs/analysis.md\`: analisi strutturale del repository
- \`docs/todo.md\`: issue e miglioramenti proposti
- \`docs/test-plan.md\`: piano di test suggerito

## Cosa osservare

- Il modello comprende la struttura complessiva del progetto?
- Le issue proposte sono concrete e attuabili?
- I suggerimenti di test coprono i casi d\'uso principali?
- Il workflow e\' ripetibile su repository diversi?

## Estensioni future

- Workflow completamente automatizzato (script bash/Python)
- Generazione automatica di codice (test, fix) con revisione umana
- Integrazione con GitHub Issues API
- Benchmark leggeri tra modelli Qwen sulle stesse task
