from logic import analyze
from output import chat_output

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

console.print(
    Panel(
        "AI chat analyzer built with [bold green]Python[/bold green] & [bold green]Ollama.[/bold green]\n"
        "[bold green][ chat path ][/bold green] - path to your chat export.\n"
        "[bold green][ model ][/bold green] - model used. Default: [bold cyan]qwen3.5:9b[/bold cyan]\n"
        "[bold green][ context size ][/bold green] - amount of context for the model. Default: [bold cyan]8192[/bold cyan]",
        title="[bold] NAVI CHAT ANALYST [/bold]",
        border_style="green",
        padding=(1, 3),
    )
)

while True:

    choice = Prompt.ask(
        choices=["analyze", "quit"],
        default="analyze",
    )

    if choice == "analyze":
        chat_path = Prompt.ask(
            "[bold green]chat path[/bold green]"
        )
        model = Prompt.ask(
            "[bold green]model[/bold green]",
            default="qwen3.5:9b"
        )
        context_size = Prompt.ask(
            "[bold green]context size[/bold green]",
            default="8192"
        )
    elif choice == "quit":
        break

    result = analyze(chat_path, model, int(context_size))

    chat_output(result)