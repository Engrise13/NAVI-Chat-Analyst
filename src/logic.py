import ollama
import json

from pathlib import Path
from model_data import user_prompt, system_prompt, output_schema

def analyze(chat_path, model, context):
    chat_path = Path(chat_path)

    if not chat_path.is_file():
        raise FileNotFoundError(f"Chat file does not exist: {chat_path}")

    chat = chat_path.read_text(encoding="utf-8")

    if not chat.strip():
        raise ValueError("Chat file is empty")

    input_prompt = f"""
{user_prompt}
<chat>
{chat}
</chat>
"""

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

    result = json.loads(response.message.content)
    return result
