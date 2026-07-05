from __future__ import annotations

CHAT_SYSTEM_PROMPT = (
    "Sei Qwen, un assistente utile per sviluppatori. "
    "Rispondi in italiano in modo chiaro, concreto e sintetico."
)

TUTOR_SYSTEM_PROMPT = (
    "Sei un developer tutor esperto. "
    "Analizza il codice ricevuto e rispondi sempre in italiano. "
    "Organizza la risposta in tre sezioni: "
    "1) Spiegazione del codice, "
    "2) Miglioramenti suggeriti, "
    "3) Test unitario semplice."
)



VISION_SYSTEM_PROMPT = (
    "Sei Qwen, un assistente con capacita' multimodali. "
    "Analizza l'immagine ricevuta e rispondi in italiano "
    "in modo chiaro, concreto e sintetico."
)


def build_vision_messages(
    image_base64: str, prompt: str, media_type: str = "image/png"
) -> list[dict]:
    return [
        {"role": "system", "content": VISION_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt.strip()},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{image_base64.strip()}"
                    },
                },
            ],
        },
    ]


def build_chat_messages(prompt: str) -> list[dict[str, str]]:
    cleaned_prompt = prompt.strip()
    return [
        {"role": "system", "content": CHAT_SYSTEM_PROMPT},
        {"role": "user", "content": cleaned_prompt},
    ]


def build_tutor_messages(code_snippet: str, language_hint: str | None = None) -> list[dict[str, str]]:
    language_line = f"Linguaggio suggerito: {language_hint}.\n" if language_hint else ""
    user_prompt = (
        f"{language_line}"
        "Analizza questo snippet di codice.\n\n"
        "Richieste:\n"
        "- spiegalo in italiano;\n"
        "- suggerisci miglioramenti pratici;\n"
        "- proponi un test unitario semplice.\n\n"
        "Codice:\n"
        "```text\n"
        f"{code_snippet.strip()}\n"
        "```"
    )
    return [
        {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

