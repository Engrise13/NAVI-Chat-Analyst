import json
from pathlib import Path
from typing import Any

import ollama

from model_data import output_schema, system_prompt, user_prompt


def ask_llm(
    prompt: str,
    content: str,
    model: str,
    context: int = 8192,
    schema: dict[str, Any] | None = None,
) -> str:
    options = {
        "num_ctx": context,
        "temperature": 0.2,
        "think": False,
    }

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
        "options": options,
        "stream": False,
    }

    if schema:
        kwargs["format"] = schema

    response = ollama.chat(**kwargs)
    return response["message"]["content"]


def msg_slice(input_text: str, part_size: int = 500, overlap: int = 50) -> list[str]:
    lines = input_text.splitlines()
    ready_parts = []
    step = max(1, part_size - overlap)

    for i in range(0, len(lines), step):
        part = lines[i : i + part_size]
        ready_parts.append("\n".join(part))

        if i + part_size >= len(lines):
            break

    return ready_parts


def chat_parse(chat_path: str | Path) -> str:
    path = Path(str(chat_path).strip("'\""))
    if not path.is_file():
        raise FileNotFoundError(f"chat file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            json_content = json.load(file)
    except (ValueError, UnicodeDecodeError):
        return path.read_text(encoding="utf-8").strip()

    messages = json_content.get("messages", [])
    lines = []

    for msg in messages:
        if msg.get("type") != "message":
            continue

        sender = msg.get("from", "неизвестный")
        date = msg.get("date", "неизвестно когда").replace("T", " ")[:16]
        text = msg.get("text", "")

        if isinstance(text, list):
            normal_parts = [
                part if isinstance(part, str) else part.get("text", "") for part in text
            ]
            text = "".join(normal_parts)

        # схлопываем переносы внутри сообщения: 1 сообщение = строго 1 строка
        text = " ".join(text.split())
        if text:
            lines.append(f"[{date}] {sender}: {text}")

    return "\n".join(lines)


def analyze(
    chat: str, model: str, context: int = 8192, max_messages: int = 10000
) -> dict[str, Any]:
    if not chat.strip():
        raise ValueError("Chat is empty!")

    # берем свежие последние max_messages сообщений
    lines = chat.splitlines()
    if len(lines) > max_messages:
        chat = "\n".join(lines[-max_messages:])

    parts = msg_slice(chat)
    if not parts:
        raise ValueError("Chat has no readable messages!")

    try:
        if len(parts) == 1:
            input_prompt = f"{user_prompt}\n<chat>\n{parts[0]}\n</chat>"
            raw_response = ask_llm(
                prompt=system_prompt,
                content=input_prompt,
                model=model,
                context=context,
                schema=output_schema,
            )
        else:
            summaries = []
            part_prompt = "сделай краткую выжимку фрагмента переписки на 2-3 предложения: ключевые события, факты, темы и динамику общения."

            for idx, part in enumerate(parts, 1):
                summary = ask_llm(
                    prompt=part_prompt,
                    content=part,
                    model=model,
                    context=context,
                )
                summaries.append(f"--- часть {idx} ---\n{summary}")

            combined_summary = "\n\n".join(summaries)
            final_content = f"{user_prompt}\n<chat_summaries>\n{combined_summary}\n</chat_summaries>"

            raw_response = ask_llm(
                prompt=system_prompt,
                content=final_content,
                model=model,
                context=context,
                schema=output_schema,
            )

    except Exception as error:
        raise RuntimeError(f"failed to communicate with ollama: {error}") from error

    try:
        return json.loads(raw_response)
    except Exception as error:
        raise ValueError(
            f"model returned invalid json: {error}\nraw output:\n{raw_response}"
        ) from error
