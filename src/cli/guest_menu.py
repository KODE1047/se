# /src/cli/guest_menu.py
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from cli.ui import console
from services import search_service
import data

def run_guest_menu():
    """
    Displays the menu for Guest users (Read-Only).
    """
    while True:
        console.print(Panel(
            "[bold]Guest Access[/bold]\n\n"
            "  [1] List All Books\n"
            "  [2] Search Books\n"
            "  [0] Back to Main Menu",
            title="--- Guest Menu ---",
            border_style="white"
        ))

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "0"], default="1")

        if choice == '1':
            handle_list_books()
        elif choice == '2':
            handle_search_books()
        elif choice == '0':
            break

def handle_list_books():
    """Lists all books."""
    display_books(data.books)

def handle_search_books():
    """Search interface."""
    console.print("\n[bold]--- Search Books ---[/bold]")
    console.print("[dim]Leave fields empty to skip.[/dim]")
    
    title = Prompt.ask("Title").strip() or None
    author = Prompt.ask("Author").strip() or None
    year_str = Prompt.ask("Year").strip()
    year = int(year_str) if year_str.isdigit() else None

    results = search_service.search_books(title=title, author=author, year=year)
    display_books(results)

def display_books(books):
    """Helper to print book table."""
    if not books:
        console.print("[yellow]No books found.[/yellow]")
        return

    table = Table(title=f"Found {len(books)} Books")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Author", style="blue")
    table.add_column("Year", style="green")
    table.add_column("Status", style="yellow")

    for book in books:
        status = "Available" if book.is_available else "On Loan"
        table.add_row(str(book.book_id), book.title, book.author, str(book.publication_year), status)
    
    console.print(table)
