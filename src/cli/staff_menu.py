# /src/cli/staff_menu.py
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from cli.ui import console
from services import book_service, loan_service
import data
from models.borrow import LoanStatus

def run_staff_menu():
    while True:
        console.print(Panel(
            "[bold]Staff Controls[/bold]\n\n"
            "  [1] Register New Book\n"
            "  [2] Manage Loan Requests\n"
            "  [3] List All Books\n"
            "  [0] Back",
            title="--- Staff Menu ---",
            border_style="yellow"
        ))

        choice = Prompt.ask("Choice", choices=["1", "2", "3", "0"], default="1")

        if choice == '1':
            handle_add_book()
        elif choice == '2':
            handle_loan_management()
        elif choice == '3':
            handle_list_books()
        elif choice == '0':
            break

def handle_add_book():
    title = Prompt.ask("Title")
    author = Prompt.ask("Author")
    year = IntPrompt.ask("Year")
    try:
        bk = book_service.add_book(title, author, year)
        console.print(f"[green]Added:[/green] {bk.title}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

def handle_list_books():
    # Simplified list
    for b in data.books:
        console.print(f"{b.title} ({b.author}) - {'Available' if b.is_available else 'Out'}")

def handle_loan_management():
    # Filter pending requests
    pending = [r for r in data.loans if r.status == LoanStatus.PENDING]
    
    if not pending:
        console.print("[green]No pending requests.[/green]")
        return

    table = Table(title="Pending Loans")
    table.add_column("Request ID", style="cyan")
    table.add_column("Book ID", style="magenta")
    table.add_column("Student ID", style="blue")
    
    for r in pending:
        table.add_row(str(r.request_id), str(r.book_id), str(r.student_id))
    console.print(table)

    req_id_str = Prompt.ask("Enter Request ID to APPROVE (or Enter to cancel)")
    if not req_id_str:
        return

    try:
        from uuid import UUID
        req_id = UUID(req_id_str)
        loan_service.approve_loan(req_id)
        console.print("[bold green]Loan Approved! Book marked as unavailable.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error processing approval:[/bold red] {e}")
