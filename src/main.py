import argparse
import ollama

from pathlib import Path
from prompt import mode_prompts, system_prompt

# Chat file path and model are required, mode and context size have defaults
parser = argparse.ArgumentParser()
parser.add_argument("--chat", help="Path to chat export file", required=True)
parser.add_argument("--model", help="Model to use for analysis", required=True)
parser.add_argument("--mode", help="Analysis mode", choices=list(mode_prompts.keys()), default="Default")
parser.add_argument("--context", help="Model context size", type=int, default=8192)
args = parser.parse_args()

# Check if the chat file exists and read its content
chat_path = Path(args.chat)
if not chat_path.is_file():
    parser.error(f"Chat file does not exist: {chat_path}")
chat = chat_path.read_text(encoding="utf-8")

prompt = f"""
{mode_prompts[args.mode]}
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
            "content": prompt,
        },
    ],
    stream=True, # Stream the response in real time
    think=False, # Prevent additional reasoning
    options={
        "num_ctx": args.context,
        "temperature": 0.2, # Lower temperature for the model to be more consistent
    },
)

for chunk in response:
    print(chunk["message"]["content"], end="", flush=True)

print() # New line at the end of the output