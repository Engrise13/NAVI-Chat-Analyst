import json
from pathlib import Path
from typing import Any

from openai import OpenAI
from pydantic import ValidationError

from model_data import OutputSchema, system_prompt


def chat_parse(chat_path: str | Path) -> str:
    path = Path(str(chat_path).strip("'\""))  # strip quotes from path
    if not path.is_file():
        raise FileNotFoundError(f"Сhat file not found: {path}")

    content = path.read_text(
        encoding="utf-8", errors="replace"
    )  # replace invalid characters
    try:
        json_content = json.loads(content)
    except json.JSONDecodeError:
        return content.strip()  # fallback to raw text if not valid json

    messages = json_content.get("messages", [])
    if not isinstance(messages, list):
        return content.strip()  # fallback if 'messages' is not a list
    lines = []

    for msg in messages:
        if (
            not isinstance(msg, dict) or msg.get("type") != "message"
        ):  # skip non-message entries
            continue

        sender = msg.get("from", "неизвестный")
        date = str(msg.get("date", "неизвестно когда")).replace("T", " ")[
            :16
        ]  # format to 'YYYY-MM-DD HH:MM' (up to minutes)
        raw_text = msg.get("text", "")

        if isinstance(raw_text, list):  # combine text parts
            parts = []
            for item in raw_text:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    parts.append(str(item.get("text", "")))
            text = "".join(parts)
        else:
            text = str(raw_text)

        clean_text = " ".join(text.split())
        if clean_text:
            lines.append(f"[{date}] {sender}: {clean_text}")  # record formatted line

    return "\n".join(lines)


def analyze(
    provider_url: str,
    api_key: str,
    model_name: str,
    chat_text: str,
    message_number: int,
) -> dict[str, Any]:
    client = OpenAI(api_key=api_key, base_url=provider_url)
    lines = chat_text.splitlines()[-message_number:]  # take last N lines
    chat = "\n".join(lines)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"\n<chat>\n{chat}\n</chat>"},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    content = response.choices[0].message.content  # get response content
    if not content:
        raise ValueError("Model could not analyze chat!")
    try:
        schema_response = OutputSchema.model_validate_json(
            content
        )  # parse and validate json
    except ValidationError as e:
        raise ValueError("JSON Validation Error!") from e
    return schema_response.model_dump()  # convert to dict
