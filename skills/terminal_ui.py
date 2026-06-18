from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text

console = Console()

def display_system_boot(status_text):
    """Renders an Iron Man themed initialization banner on startup."""
    banner = Text("🔴 SPIRIT MARK I PROTOCOL ONLINE 🔴\n", style="bold bright_red")
    banner.append(f"Core Engine: {status_text}", style="bold bright_yellow")
    console.print(Panel(banner, border_style="bright_red", expand=False))

def display_user_input(text):
    """Displays user commands cleanly minimized."""
    console.print(f"\n[bold bright_yellow]🗣️ You:[/bold bright_yellow] [italic]{text}[/italic]")

def display_agent_response(plain_text):
    """Renders full markdown formatting, syntax highlighting, and text styles."""
    md_content = Markdown(plain_text)
    
    console.print("\n[bold bright_red]⚡ SPIRIT:[/bold bright_red]")
    console.print(Panel(md_content, border_style="bright_yellow", padding=(1, 2)))

def display_standby():
    """Prints a clean status line showing the engine is sleeping."""
    console.print("[dim bright_red]💤 Arc Reactor in Standby... Listening for 'SPIRIT'[/dim bright_red]", end="\r")