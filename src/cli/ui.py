# /src/cli/ui.py
from rich.console import Console  # <-- This line was missing

# Create a single, shared Console instance for consistent styling
console = Console()