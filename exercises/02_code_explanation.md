# 02 - Code Explanation

## Obiettivo

Passare uno snippet Python al Developer Tutor e ottenere:

- spiegazione in italiano;
- suggerimenti di miglioramento;
- un test unitario semplice.

## Snippet suggerito

Usa `examples/simple_function.py` oppure questo frammento:

```python
def is_even(number: int) -> bool:
    return number % 2 == 0
```

## Cosa osservare

- La spiegazione e' corretta e comprensibile?
- I miglioramenti proposti sono pratici?
- Il test unitario copre il comportamento atteso?

## Modalita' consigliate

- CLI con `python -m qwen_dev_tutor code-review examples/simple_function.py`
- endpoint `POST /tutor`

