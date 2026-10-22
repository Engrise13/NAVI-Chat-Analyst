import argparse
import ollama
import json

from pathlib import Path
from model_data import user_prompt, system_prompt, output_schema

# Chat file path and model are required, mode and context size have defaults
parser = argparse.ArgumentParser()
parser.add_argument("--chat", help="Path to chat export file", required=True)
parser.add_argument("--model", help="Model to use for analysis", required=True)
parser.add_argument("--context", help="Model context size", type=int, default=8192)
args = parser.parse_args()

# Check if the chat file exists and read its content
chat_path = Path(args.chat)
if not chat_path.is_file():
    parser.error(f"Chat file does not exist: {chat_path}")
chat = chat_path.read_text(encoding="utf-8")

input_prompt = f"""
{user_prompt}
<chat>
{chat}
</chat>
"""

response = ollama.chat(
    model=args.model,
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": input_prompt,
        },
    ],
    format=output_schema,
    stream=False,
    think=False,
    options={
        "num_ctx": args.context,
        "temperature": 0.2,
    },
)

result = json.loads(response.message.content)

print(json.dumps(result, ensure_ascii=False, indent=2))