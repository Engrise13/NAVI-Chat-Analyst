from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt

from logic import analyze, chat_parse
from output import chat_output

console = Console()
console.clear()

start_text = """
chat analysis engine built with [bold cyan]Python[/]
[bold magenta]details needed:[/]
• [bold green]provider URL[/]       OpenAI-compatible endpoint
• [bold green]API key[/]            model access token
• [bold green]model name[/]         target LLM identifier
• [bold green]chat export file[/]   Telegram .json or plain .txt log
• [bold green]message number[/]     lines from the end (5000 is safe default)
"""

start_message = Panel(
    start_text, title="NAVI chat analyst v1.0", border_style="bold green"
)


console.print(start_message)

while True:
    try:
        action = Prompt.ask(
            "[bold green]choose action[/]",
            choices=["analyze", "quit"],
            default="analyze",
        )

        if action == "quit":
            console.print("[dim]выход...[/]")
            break

        provider_url = Prompt.ask("[bold green]provider URL[/]")

        api_key = Prompt.ask("[bold green]API key[/]")

        model_name = Prompt.ask("[bold green]model name[/]")

        chat_export = Prompt.ask("[bold green]chat export file[/]")

        message_number = IntPrompt.ask(
            "[bold green]message number[/]",
            default=5000,
        )

        chat_text = chat_parse(chat_export)
        with console.status("[bold cyan]analyzing...[/]"):
            result = analyze(
                chat_text, message_number, provider_url, api_key, model_name
            )
        chat_output(result)

    except KeyboardInterrupt:
        console.print("\n[red]Forcequit![/]")
        break

    except Exception as error:  # noqa: BLE001
        console.print(f"[red]{error}[/]")
