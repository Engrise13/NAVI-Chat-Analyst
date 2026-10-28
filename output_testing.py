from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns

sample_output = {
    "summary": "The conversation focused on developing a chat analysis tool using Python and Ollama.",
    "primary_intent": "Develop and improve a chat analysis application.",
    "key_topics": [
        "Python development",
        "Ollama integration",
        "JSON output schema",
        "Rich terminal interface",
        "Data visualization"
    ],
    "emotional_tone": "Neutral and task-oriented",
    "outcomes_and_open_questions": [
        "A structured JSON schema was defined for analysis results.",
        "The CLI will use Rich for formatted output.",
        "PyQtGraph may be used for data visualization."
    ],
    "scores": {
        "intent_clarity": 90,
        "relevance": 95,
        "constructive_quality": 88,
        "mutual_understanding": 85,
        "goal_progress": 75
    }
}

console = Console()

card1 = Panel(
    "Conversation summary goes here.",
    title="Summary",
    border_style="green",
)

card2 = Panel(
    "Planning and development.",
    title="Primary Intent",
    border_style="yellow",
)

console.print(Columns([card1, card2], equal=True, expand=True))