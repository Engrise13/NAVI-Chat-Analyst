from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns

def score_color(num):
    num = max(0, min(100, num))
    if num <= 50:
        red = 255
        green = int(255 * num / 50)
    else:
        red = int(255 * (100 - num) / 50)
        green = 255
    return f"bold #{red:02x}{green:02x}00"

console = Console()

def chat_output(input_json):
    summary = Panel(
        f"[bold green]{input_json["summary"]}[/bold green]",
        title="chat summary",
        border_style="bold green"
    )

    intent = Panel(
        f"[bold cyan]{input_json["primary_intent"]}[/bold cyan]",
        title="primary intent",
        border_style="bold cyan"
    )

    emotional_tone = Panel(
        f"[bold cyan]{input_json["emotional_tone"]}[/bold cyan]",
        title="emotional tone",
        border_style="bold cyan"
    )

    topics_card = Panel(
        "\n".join(
            f"[bold magenta]{item}[/bold magenta]"
            for item in input_json["key_topics"]
        ),
        title="key topics",
        border_style="bold magenta"
    )

    scores_card = Panel(
        "\n".join(    
            f"[bold magenta]{key}:[/bold magenta] [{score_color(value)}]{value}%[/{score_color(value)}]"
            for key, value in input_json["scores"].items()
        ),
        title="chat scores",
        border_style="bold magenta"
    )

    outcomes = Panel(
        "\n".join(
            f"[bold green]{item}[/bold green]"
            for item in input_json["outcomes_and_open_questions"]
        ),
        title="outcomes and open questions",
        border_style="bold green"
    )

    console.print(summary)
    console.print(intent)
    console.print(emotional_tone)
    console.print(Columns([topics_card, scores_card], equal=True, expand=True))
    console.print(outcomes)