from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from logic import analyze, chat_parse
from output import chat_output

console = Console()

console.print(
    Panel(
        "AI chat analyzer built with [bold green]Python[/] & [bold green]Ollama.[/]\n"
        "[bold green][ chat path ][/] - path to your chat export.\n"
        "[bold green][ model ][/] - model used. Default: [bold cyan]qwen3.5:9b[/]\n"
        "The program is calibrated to run at [bold green]8192[/] model tokens.\n"
        "The program can process up to [bold green]10k[/] chat messages at once.\n",
        title="[bold] NAVI CHAT ANALYST [/]",
        border_style="green",
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
        try:
            with console.status("[bold magenta]analyzing chat with ollama...[/]"):
                parsed_chat = chat_parse(chat_path)
                result = analyze(parsed_chat, model, 8192)
            chat_output(result)
        except (FileNotFoundError, ValueError, RuntimeError) as error:
            console.print(f"[red]{error}[/]")

    elif choice == "quit":
        break
