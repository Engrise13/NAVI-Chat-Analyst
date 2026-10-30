from typing import Any

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

console = Console()


def score_color(num: int) -> str:
    num = max(0, min(100, num))
    if num <= 50:
        red = 255
        green = int(255 * num / 50)
    else:
        red = int(255 * (100 - num) / 50)
        green = 255
    return f"bold #{red:02x}{green:02x}00"


def chat_output(input_json: dict[str, Any]) -> None:
    summary = Panel(
        f"[bold green]{input_json.get('summary', '')}[/]",
        title="chat summary",
        border_style="bold green",
    )

    intent = Panel(
        f"[bold cyan]{input_json.get('primary_intent', '')}[/]",
        title="primary intent",
        border_style="bold cyan",
    )

    emotional_tone = Panel(
        f"[bold cyan]{input_json.get('emotional_tone', '')}[/]",
        title="emotional tone",
        border_style="bold cyan",
    )

    key_topics = input_json.get("key_topics", [])
    topics_card = Panel(
        "\n".join(f"[bold magenta]• {item}[/]" for item in key_topics)
        if key_topics
        else "[dim red]None[/]",
        title="key topics",
        border_style="bold magenta",
    )

    scores_card = Panel(
        "\n".join(
            f"[bold magenta]{key}:[/] [{score_color(value)}]{value}%[/]"
            for key, value in input_json.get("scores", {}).items()
        ),
        title="chat scores",
        border_style="bold magenta",
    )

    outcomes = input_json.get("outcomes_and_open_questions", [])
    outcomes_card = Panel(
        "\n".join(f"[bold green]• {item}[/]" for item in outcomes)
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
