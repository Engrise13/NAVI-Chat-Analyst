from sys import exit
from logic import analyze

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
    exit()

result = analyze(chat_path, model, int(context_size))

for x in result.keys():
    print(f"{x}: {result[x]}")

## normal output still needed