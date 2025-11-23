# /src/cli/staff_menu.py
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

from services import book_service  
from cli.ui import console         
import data as data                

def run_staff_menu():
    """
    Displays the menu for Library Staff members.
    """
    while True:
        console.print(Panel(
            "[bold]What would you like to do?[/bold]\n\n"
            "  [1] Register New Book (Req 3-3)\n"
            "  [2] List All Books (Testing)\n"
            "  [0] Back to Main Menu",
            title="--- Library Staff Menu ---",
            border_style="yellow"
        ))
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "0"], default="1")
        
        if choice == '1':
            handle_add_book()
        elif choice == '2':
            handle_list_books()
        elif choice == '0':
            console.print("[dim]Returning to Main Menu...[/dim]")
            break

def handle_add_book():
    """Handles the UI for adding a new book."""
    console.print("\n[bold]--- Register New Book ---[/bold]")
    try:
        title = Prompt.ask("Enter title").strip()
        author = Prompt.ask("Enter author").strip()
        
        # Use IntPrompt for automatic validation
        publication_year = IntPrompt.ask("Enter publication year")
        
        if not title or not author:
            console.print("[danger]Error: Title and author fields are required.[/danger]")
            return
            
        new_book = book_service.add_book(
            title=title,
            author=author,
            publication_year=publication_year
        )
        console.print(f"\n[bold green]Success: Book '{new_book.title}' added with ID: {new_book.book_id}[/bold green]")
        
    except Exception as e:
        console.print(f"[danger]An error occurred: {e}[/danger]")

def handle_list_books():
    """(For testing) Displays all books currently in the system."""
    console.print("\n[bold]--- All Registered Books ---[/bold]")
    if not data.books:
        console.print("[yellow]No books registered yet.[/yellow]")
        return
        
    table = Table(title="Registered Books")
    table.add_column("Book ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Author", style="blue")
    table.add_column("Year", justify="right", style="green")
    table.add_column("Status", justify="right", style="yellow")

    for book in data.books:
        status = "Available" if book.is_available else "On Loan"
        table.add_row(
            str(book.book_id),
            book.title,
            book.author,
            str(book.publication_year),
            status
        )
        
    console.print(table)