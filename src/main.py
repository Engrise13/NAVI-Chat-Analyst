from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt

from logic import analyze
from output import chat_output

console = Console()

console.print(
    Panel(
        "AI chat analyzer built with [bold green]Python[/] & [bold green]Ollama.[/]\n"
        "[bold green][ chat path ][/] - path to your chat export.\n"
        "[bold green][ model ][/] - model used. Default: [bold cyan]qwen3.5:9b[/]\n"
        "[bold green][ context size ][/] - amount of context for the model. Default: [bold cyan]8192[/]",
        title="[bold] NAVI CHAT ANALYST [/]",
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
        chat_path = Prompt.ask("[bold green]chat path[/]")
        model = Prompt.ask("[bold green]model[/]", default="qwen3.5:9b")
        context_size = IntPrompt.ask("[bold green]context size[/]", default="8192")
        try:
            with console.status("[bold magenta]analyzing chat with ollama...[/]"):
                result = analyze(chat_path, model, context_size)
            chat_output(result)
        except (FileNotFoundError, ValueError, RuntimeError) as error:
            console.print(f"[bold red]error:[/] {error}")

    elif choice == "quit":
        break
