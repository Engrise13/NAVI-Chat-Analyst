from typing import Any

from rich.columns import Columns
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

console = Console()


def score_color(num: Any) -> str:
    try:
        val = int(num)
    except (TypeError, ValueError):
        val = 50

    val = max(0, min(100, val))
    if val <= 50:
        red = 255
        green = int(255 * val / 50)
    else:
        red = int(255 * (100 - val) / 50)
        green = 255
    return f"bold #{red:02x}{green:02x}00"


def chat_output(input_json: dict[str, Any]) -> None:
    summary_text = escape(str(input_json.get("summary", "")))
    summary = Panel(
        summary_text,
        title="chat summary",
        border_style="bold green",
    )

    intent_text = escape(str(input_json.get("primary_intent", "")))
    intent = Panel(
        intent_text,
        title="primary intent",
        border_style="bold cyan",
    )

    tone_text = escape(str(input_json.get("emotional_tone", "")))
    emotional_tone = Panel(
        tone_text,
        title="emotional tone",
        border_style="bold cyan",
    )

    key_topics = input_json.get("key_topics", [])
    topics_card = Panel(
        "\n".join(f"[bold magenta]• {escape(str(item))}[/]" for item in key_topics)
        if key_topics
        else "[dim red]None[/]",
        title="key topics",
        border_style="bold magenta",
    )

    scores = input_json.get("scores", {})
    scores_lines = []
    if isinstance(scores, dict):
        for key, value in scores.items():
            scores_lines.append(
                f"[bold magenta]{escape(str(key))}:[/] [{score_color(value)}]{value}%[/]"
            )

    scores_card = Panel(
        "\n".join(scores_lines) if scores_lines else "[dim red]None[/]",
        title="chat scores",
        border_style="bold magenta",
    )

    outcomes = input_json.get("outcomes_and_open_questions", [])
    outcomes_card = Panel(
        "\n".join(f"[bold green]• {escape(str(item))}[/]" for item in outcomes)
        if outcomes
        else "[dim red]None[/]",
        title="outcomes and open questions",
        border_style="bold green",
    )

    console.print(summary)
    console.print(intent)
    console.print(emotional_tone)
    console.print(Columns([topics_card, scores_card], equal=True, expand=True))
    console.print(outcomes_card)
