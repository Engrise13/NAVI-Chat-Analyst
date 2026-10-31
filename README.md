# NAVI Chat Analyst

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/OpenAI_API-Compatible-412991?style=flat-square&logo=openai&logoColor=white" alt="OpenAI API Compatible" />
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic v2" />
  <img src="https://img.shields.io/badge/Rich-CLI-00D26A?style=flat-square" alt="Rich CLI" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License" />
</p>

CLI-based communication analysis engine powered by OpenAI-compatible LLM endpoints. Parses raw dialogue history, enforces structured JSON output via Pydantic schemas, and renders quantified conversational metrics in the terminal.

---

## Key Features

- **Provider Agnostic:** Connects to any OpenAI-compatible API (OpenAI, OpenRouter, vLLM, LocalAI, Ollama, etc.) via custom `base_url` and token.
- **Dual Log Parsing:** Ingests Telegram export dumps (`result.json`) and raw plaintext logs (`.txt`).
- **Tail-Slicing Window:** Truncates analysis to the last $N$ lines (default: 5000) to respect target token limits.
- **Strict Schema Enforcement:** LLM outputs are constrained to `json_object` and validated through strict Pydantic v2 schemas (`extra="forbid"`).
- **Dynamic Terminal UI:** Color-coded gradient output (0–100%) and formatted metric cards powered by `rich`.

---

## Technical Architecture

```text
[Telegram JSON / Plain TXT]
            │
            ▼
     chat_parse()          --> Extracts timestamps, normalize senders & strings
            │
            ▼
      analyze()            --> Slices last N lines, sets temperature=0.2,
            │                  requests json_object via OpenAI client
            ▼
    OutputSchema (Pydantic)--> Enforces field boundaries, types, and forbids extras
            │
            ▼
     chat_output()         --> Renders UI panels and color-scaled metrics
```

### Validated Metric Schema

The model scores communication parameters on a `0–100` scalar scale:

| Metric | Focus |
| :--- | :--- |
| `intent_clarity` | Precision and absence of ambiguity in user queries. |
| `relevance` | Dialogue adherence to main subject without off-topic drift. |
| `constructive_quality` | Problem-solving efficiency, lack of toxicity or friction. |
| `mutual_understanding` | Context retention, lack of redundant re-clarifications. |
| `goal_progress` | Measurable advancement toward the stated `primary_intent`. |

---

## Requirements

- Python `3.10+`
- Valid endpoint for an OpenAI-compatible API provider

Install dependencies:

```bash
pip install openai pydantic rich
```

---

## Usage

Run the entry point script:

```bash
python main.py
```

### CLI Parameters

Upon selecting `analyze`, provide the following prompts:

| Prompt | Description | Example |
| :--- | :--- | :--- |
| `provider URL` | Base URL of the OpenAI-compatible endpoint | `https://api.openai.com/v1` or `http://localhost:11434/v1` |
| `API key` | API access key / bearer token | `sk-...` |
| `model name` | Target model identifier | `gpt-4o-mini`, `qwen2.5:72b` |
| `chat export file` | Absolute or relative path to log file | `chat.json` or `logs/dialogue.txt` |
| `message number` | Number of tail lines to evaluate | `5000` |

---

## Schema Contract

The engine outputs and validates against the following data structure:

```json
{
  "summary": "string (2-4 sentences, factual overview)",
  "primary_intent": "string (core initial objective)",
  "key_topics": ["string (1-3 words each, 1 to 5 items)"],
  "emotional_tone": "string (observed emotional state)",
  "outcomes_and_open_questions": ["string (1 to 5 items)"],
  "scores": {
    "intent_clarity": 85,
    "relevance": 90,
    "constructive_quality": 80,
    "mutual_understanding": 75,
    "goal_progress": 85
  }
}
```

---

## Project Structure

```text
├── main.py        # CLI interface and runtime loop
├── logic.py       # File parsers (JSON/TXT) and LLM inference pipeline
├── model_data.py  # Pydantic schemas (Scores, OutputSchema) and system prompt
└── output.py     # Rich terminal styling and score-to-color mapping
```

---

## License

MIT