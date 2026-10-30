# NAVI Chat Analyst

[![Python](https://img.shields.io/badge/Python-3.x-007ACC?logo=python&logoColor=white)](#)
[![Version](https://img.shields.io/badge/version-1.0-orange)](#)
[![Status](https://img.shields.io/badge/status-in%20development-gold)](#)
[![Platform](https://img.shields.io/badge/platform-any-lightgrey)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](#)

Local LLM-powered dialogue analysis engine built on top of Python and Ollama. Evaluates chat logs, extracts structured intent, emotional tone, outcomes, and computes quantified communication metrics via JSON Schema enforcement.

---

## Technical Specifications

- **Execution Mode:** Local execution (offline, no external network calls).
- **Target Context Window:** Calibrated for `8192` model tokens.
- **Throughput / Capacity:** Scaled to process batches of up to `10,000` messages.
- **Chunking Pipeline:** Overlapping sliding window (`part_size=500`, `overlap=50`) with recursive chunk summarization for extended logs.
- **Inference Runtime:** [Ollama](https://ollama.com/) (recommended default: `qwen3.5:9b`).
- **Input Formats:** Telegram JSON export format or plain raw `.txt` chat dumps.

---

## Architecture & Analysis Pipeline

1. **Ingestion & Normalization:** `chat_parse` standardizes timestamps, sender metadata, and multi-part string entities into single-line uniform logs.
2. **Context Window Slicing:** Long histories exceeding window limits are split into overlapping chunks, recursively summarized, and aggregated into a high-level representation.
3. **Structured Inference:** Extracted chat tokens are evaluated against a strict JSON Schema returning:
   - `summary`: Objective overview of the interaction.
   - `primary_intent`: Core driver of the dialogue initiator.
   - `key_topics`: Clustered agenda items and friction points.
   - `emotional_tone`: Observed conversational temperature and sentiment.
   - `outcomes_and_open_questions`: Explicit agreements, action items, and unresolved questions.
   - `scores`: Quantified scalar metrics (0–100): `intent_clarity`, `relevance`, `constructive_quality`, `mutual_understanding`, `goal_progress`.
4. **Terminal Formatting:** Rendered using sanitized [Rich](https://github.com/Textualize/rich) panel components.

---

## Dependencies

- Python `3.10+`
- [ollama](https://pypi.org/project/ollama/)
- [rich](https://pypi.org/project/rich/)

Install dependencies:

```bash
pip install ollama rich
```

Ensure Ollama is running and the target model is pulled:

```bash
ollama serve
ollama pull qwen3.5:9b
```

---

## Usage

Launch interactive CLI:

```bash
python main.py
```

Prompts:
1. `choice`: select `analyze` or `quit`.
2. `chat path`: path to input file (`.json` or `.txt`).
3. `model`: Ollama model tag (default: `qwen3.5:9b`).

---

## Output Contract

Responses conform to standard structured schema:

```json
{
  "summary": "string",
  "primary_intent": "string",
  "key_topics": ["string"],
  "emotional_tone": "string",
  "outcomes_and_open_questions": ["string"],
  "scores": {
    "intent_clarity": 0,
    "relevance": 0,
    "constructive_quality": 0,
    "mutual_understanding": 0,
    "goal_progress": 0
  }
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).