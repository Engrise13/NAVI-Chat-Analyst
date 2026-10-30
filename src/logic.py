import json
from pathlib import Path
from typing import Any

import ollama

from model_data import output_schema, system_prompt, user_prompt


def analyze(chat_path: str | Path, model: str, context: int) -> dict[str, Any]:
    chat_path = Path(chat_path)

    if not chat_path.is_file():
        raise FileNotFoundError(f"Chat file does not exist: {chat_path}")

    chat = chat_path.read_text(encoding="utf-8").strip()

    if not chat:
        raise ValueError(f"Chat file is empty: {chat_path}")

    input_prompt = f"{user_prompt}\n<chat>\n{chat}\n</chat>"
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_prompt},
            ],
            format=output_schema,
            stream=False,
            think=False,
            options={
                "num_ctx": context,
                "temperature": 0.2,
            },
        )

    except Exception as error:
        raise RuntimeError(f"failed to communicate with ollama: {error}") from error

    raw_response = response.message.content

    try:
        return json.loads(raw_response)
    except Exception as error:
        raise ValueError(
            f"model returned invalid json: {error}\nraw output:\n{raw_response}"
        ) from error
