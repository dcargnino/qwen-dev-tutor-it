# 03 - Model Comparison

## Obiettivo

Usare lo stesso prompt su modelli Qwen diversi per confrontare:

- qualita' della risposta;
- velocita' percepita;
- stile espositivo.

## Procedura

1. Configura un primo modello in `.env`.
2. Esegui una richiesta con CLI o UI.
3. Cambia solo `QWEN_MODEL` oppure `QWEN_BASE_URL`.
4. Ripeti lo stesso prompt.
5. Confronta i risultati manualmente.

## Prompt suggerito

```text
Spiegami le differenze tra unit test, integration test e end-to-end test con esempi Python.
```

## Note

Per questa fase il confronto resta manuale. In futuro il progetto potra' raccogliere metriche e report piu' strutturati.

