# qwen-dev-tutor-it

```text
   ____                         ____              ______      __
  / __ \__      _____  ____    / __ \___ _   __  /_  __/_  __/ /_____  _____
 / / / /\ \ /\ / / _ \/ __ \  / / / / _ \ | / /   / / / / / / __/ __ \/ ___/
/ /_/ /  \ V  V /  __/ / / / / /_/ /  __/ |/ /   / / / /_/ / /_/ /_/ / /
\___\_\   \_/\_/ \___/_/ /_/  \____/\___/|___/   /_/  \__,_/\__/\____/_/
```

> Un progetto open-source per portare Qwen dentro la developer education italiana con un approccio pratico, accessibile e pronto per workshop, community meetup e storytelling tecnico.

![Qwen model offering](assets/Qwen3.7-Max-June22.png)

> Una panoramica visiva dell'offerta Qwen, utile per contestualizzare la varietà della famiglia di modelli e il potenziale del progetto.

## Che cos'e' Qwen

Qwen non e' un solo modello.
E' una **famiglia di modelli AI** sviluppata dal team Qwen di Alibaba Cloud, con una gamma che comprende:

- **LLM general-purpose** per chat, ragionamento, scrittura e task generali;
- **modelli per coding** pensati per spiegazione, generazione e revisione di codice;
- **modelli multimodali** orientati a immagini, audio e interazioni piu' ricche;
- **varianti hosted via API** e **release open-source** che la community puo' studiare, provare e integrare.

Questo punto e' centrale per il progetto.

`qwen-dev-tutor-it` non nasce solo per "fare una chat con un modello".
Nasce per valorizzare il fatto che **Qwen e' un ecosistema ampio, pratico e in parte apertamente disponibile**, quindi adatto sia a demo rapide sia a percorsi piu' profondi di studio, sperimentazione e community building.

## Visione

`qwen-dev-tutor-it` non nasce per essere soltanto una demo.

Nasce per diventare un **ponte**:

- tra modelli e persone che vogliono davvero usarli;
- tra AI e developer education;
- tra sperimentazione personale e contenuti utili per la community;
- tra una semplice prova tecnica e un progetto che puo' crescere in workshop, tutorial, talk e iniziative ambassador.

L'idea e' semplice ma forte:

**prendere Qwen e trasformarlo in uno strumento che aiuti sviluppatori a capire meglio il codice, imparare, confrontare modelli e immaginare nuovi workflow.**

## Perche' questo progetto conta

Molti progetti AI mostrano che un modello "puo' rispondere".

Questo progetto vuole mostrare qualcosa di piu' interessante:

**come Qwen puo' essere presentato, insegnato e adottato in un contesto developer-first.**

E proprio perche' Qwen include **modelli di tipologie diverse** e una forte componente **open-source**, il progetto puo' diventare una base molto credibile per:

- spiegare la differenza tra modelli generalisti, coder e multimodali;
- mostrare cosa significa usare un modello hosted rispetto a uno eseguibile localmente;
- aiutare la community a sperimentare non solo con "un LLM", ma con un'intera famiglia di modelli.

Significa costruire qualcosa che sia:

- abbastanza semplice da essere capito in pochi minuti;
- abbastanza concreto da essere usato in una demo live;
- abbastanza pulito da essere esteso senza ripartire da zero;
- abbastanza ispirazionale da accendere idee in chi partecipa a un workshop o scopre il progetto su GitHub.

## La storia che racconta

Il messaggio centrale del repository e' questo:

```text
stesso progetto
stessi prompt
stessa esperienza

Qwen hosted oppure Qwen locale

senza cambiare il cuore dell'app
```

Questa scelta architetturale e' anche una scelta narrativa.

Rende il progetto utile per:

- mostrare Alibaba Model Studio in modo pratico;
- abbassare la soglia d'ingresso con setup locali;
- confrontare modelli e deployment in un linguaggio comprensibile alla community;
- far vedere che Qwen puo' vivere sia in ambienti managed sia in percorsi piu' maker-oriented.

Ma soprattutto rende visibile una caratteristica molto forte di Qwen:

```text
una sola famiglia
piu' tipi di modelli
piu' modi di adozione
piu' spazio per la community
```

## Il cuore dell'MVP

Il progetto parte da un caso d'uso simbolico e fortemente community-friendly:

### Developer Tutor

Uno sviluppatore incolla uno snippet.
Qwen risponde in italiano con:

1. spiegazione del codice;
2. suggerimenti di miglioramento;
3. proposta di un test unitario semplice.

In altre parole:

```text
codice grezzo
    |
    v
Qwen lo rende comprensibile
    |
    v
apprendimento, miglioramento, discussione
```

Questo e' il tipo di interazione che funziona bene in:

- workshop hands-on;
- tutorial registrati;
- mini demo durante meetup;
- contenuti educativi per chi vuole capire il valore di un coding assistant.

## Cosa dimostra oggi

- chat testuale con Qwen in italiano;
- developer tutor semplice e leggibile;
- API FastAPI minima;
- UI web minimale per test veloci;
- CLI per prompt e code review;
- prompt separati dalla logica applicativa;
- configurazione unica per hosted e local;
- esercizi documentati per apprendimento, confronto e demo.

## Cosa puo' diventare domani

`qwen-dev-tutor-it` e' pensato come base per una famiglia di esperienze community-centric:

- laboratori introduttivi su Qwen;
- workshop su prompt design per sviluppatori;
- confronti tra modelli Qwen diversi;
- demo multimodali con vision;
- scenari audio/speech;
- workflow agentici leggeri su piccoli repository;
- materiale pratico per ambassador activity, talk e community enablement.

## Architettura in un colpo d'occhio

```text
                         +----------------------+
                         |      Utente          |
                         | dev / tutor / maker  |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                                             |
             v                                             v
   +---------------------+                      +---------------------+
   | UI web minimale     |                      | CLI                 |
   | chat + code tutor   |                      | chat / code-review  |
   +----------+----------+                      +----------+----------+
              \                                         /
               \                                       /
                v                                     v
                 +-----------------------------------+
                 | qwen_dev_tutor                    |
                 | config + prompts + tutor + client |
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
| Alibaba Model    |   | Ollama / vLLM /     |   | Altri endpoint     |
| Studio           |   | LM Studio locali    |   | compatibili        |
+------------------+   +---------------------+   +--------------------+
```

## Due modalita', una sola esperienza

### 1. Qwen hosted

Uso di endpoint OpenAI-compatible, inclusa la compatibilita' con Alibaba Model Studio.

### 2. Qwen locale

Uso di modelli Qwen esposti localmente tramite server OpenAI-compatible, per esempio:

- Ollama
- vLLM
- LM Studio
- altri endpoint compatibili con `/v1/chat/completions`

Il punto non e' solo tecnico.
Il punto e' che questo rende il progetto adatto sia a contesti enterprise-friendly sia a community piu' sperimentali.

Ed e' qui che il lato open-source di Qwen conta davvero: permette di immaginare un percorso che va dalla semplice API demo fino alla sperimentazione locale, al confronto tra varianti del modello e alla costruzione di workflow condivisibili dalla community.

## Perche' si presta bene a iniziative Ambassador e community

Perche' tiene insieme quattro dimensioni che raramente convivono bene nello stesso repository:

- **accessibilita'**: si spiega facilmente anche a chi non conosce ancora Qwen;
- **utilita'**: mostra un flusso che interessa davvero chi sviluppa;
- **estendibilita'**: apre la strada a vision, audio, agent e benchmark leggeri;
- **community leverage**: e' perfetto per meetup, live coding, tutorial e contenuti educational.

Un buon progetto ambassador non deve essere solo potente.
Deve essere anche **adottabile, raccontabile e riusabile**.

Questo e' esattamente il tipo di spazio che `qwen-dev-tutor-it` vuole occupare.

## Who is this for?

Questo progetto e' pensato per persone e contesti diversi, ma con un punto in comune: la voglia di usare Qwen non come curiosita' astratta, ma come strumento concreto di apprendimento, sperimentazione e condivisione.

### Developer

Per chi vuole:

- provare Qwen su task reali legati al codice;
- confrontare facilmente setup hosted e locali;
- partire da una base semplice invece di un framework pesante;
- esplorare prompt e workflow utili per coding assistance.

### Educator e workshop creator

Per chi organizza:

- workshop introduttivi;
- laboratori hands-on;
- sessioni community;
- contenuti educativi per sviluppatori.

Il progetto offre un caso d'uso immediato, facilmente spiegabile e abbastanza compatto da essere portato in aula, in live demo o in un meetup.

### Community builder e Ambassador

Per chi vuole costruire attorno a Qwen:

- storytelling tecnico chiaro;
- demo replicabili;
- esempi open-source facili da condividere;
- percorsi progressivi che partono da chat e coding e possono crescere verso vision, audio e agentic workflows.

### Maker e sperimentatori

Per chi preferisce imparare provando:

- cambiando modello;
- cambiando endpoint;
- confrontando risposte;
- trasformando piccoli esercizi in esperimenti piu' ricchi.

In breve:

```text
se vuoi spiegare Qwen,
provare Qwen,
insegnare Qwen,
o costruire attorno a Qwen,
questo progetto e' pensato per te.
```

## Esperienza d'uso

### Chat testuale

Una richiesta semplice per verificare rapidamente:

- qualita' della risposta;
- uso dell'italiano;
- tono;
- velocita' percepita.

### Developer Tutor

Il caso d'uso piu' forte per developer education:

- spiega codice;
- suggerisce miglioramenti;
- propone un test;
- crea una base di discussione tecnica.

### Esercizi guidati

La cartella `exercises/` non e' un accessorio.
E' il seme di un percorso didattico.

Include:

- `01_text_chat.md`
- `02_code_explanation.md`
- `03_model_comparison.md`
- `04_vision_placeholder.md`
- `05_audio_placeholder.md`
- `06_agentic_workflow_placeholder.md`

Ogni esercizio aiuta a trasformare il repository da semplice MVP a strumento per attivare conversazioni, prove pratiche e nuove iterazioni.

## Setup e configurazione

### Setup rapido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
copy .env.example .env
```

### Variabili principali

- `QWEN_PROVIDER`
- `QWEN_API_KEY`
- `QWEN_BASE_URL`
- `QWEN_MODEL`

Variabili opzionali:

- `QWEN_TIMEOUT_SECONDS`
- `QWEN_ALLOW_EMPTY_API_KEY`

### Esempio Alibaba Model Studio

```env
QWEN_PROVIDER=alibaba-model-studio
QWEN_API_KEY=your-model-studio-key
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode
QWEN_MODEL=qwen-plus
QWEN_ALLOW_EMPTY_API_KEY=false
```

### Esempio Qwen locale

```env
QWEN_PROVIDER=ollama-local
QWEN_API_KEY=local-demo-key
QWEN_BASE_URL=http://localhost:11434
QWEN_MODEL=qwen2.5-coder:7b
QWEN_ALLOW_EMPTY_API_KEY=true
```

## Esempi di utilizzo

### CLI

```bash
python -m qwen_dev_tutor chat "Ciao, spiegami cos'e' FastAPI"
python -m qwen_dev_tutor code-review examples/simple_function.py
```

### API

- `GET /health`
- `POST /chat`
- `POST /tutor`
- `GET /`

### Esempio `POST /chat`

```bash
curl -X POST http://127.0.0.1:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"Spiegami FastAPI in italiano\"}"
```

### Esempio `POST /tutor`

```bash
curl -X POST http://127.0.0.1:8000/tutor ^
  -H "Content-Type: application/json" ^
  -d "{\"code\":\"def add(a, b):\n    return a + b\"}"
```

## Struttura repository

```text
qwen-dev-tutor-it/
  README.md
  .env.example
  pyproject.toml
  config/
    models.example.yaml
  exercises/
    01_text_chat.md
    02_code_explanation.md
    03_model_comparison.md
    04_vision_placeholder.md
    05_audio_placeholder.md
    06_agentic_workflow_placeholder.md
  examples/
    simple_function.py
  src/
    qwen_dev_tutor/
      __init__.py
      __main__.py
      api.py
      cli.py
      client.py
      config.py
      prompts.py
      tutor.py
  tests/
    test_config.py
    test_prompts.py
```

## Mappa del codice

| File | Ruolo |
|---|---|
| `config.py` | legge la configurazione runtime |
| `client.py` | parla con endpoint OpenAI-compatible |
| `prompts.py` | contiene i prompt del progetto |
| `tutor.py` | collega prompt e client |
| `api.py` | espone API e pagina web minima |
| `cli.py` | espone i comandi da terminale |

## Roadmap vision-driven

```text
oggi
|
|-- text chat in italiano
|-- developer tutor
|-- CLI + API minima
|-- exercises per workshop
|
v
domani
|-- vision workflow
|-- audio and speech
|-- model comparison piu' strutturato
|-- benchmark leggeri
|-- agentic workflows su mini repo
|-- toolkit per workshop e community sessions
```

## Perche' qwen-dev-tutor-it

Perche' ha il giusto equilibrio tra ambizione e pragmatismo.

Non promette troppo.
Non prova a essere tutto.
Ma apre una direzione chiara:

**rendere Qwen piu' vicino alla pratica quotidiana di chi sviluppa, insegna, condivide e costruisce community.**
