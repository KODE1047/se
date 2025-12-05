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
            "  [2] Manage Loan Requests (Approve)\n"
            "  [3] Return Book (Check-in)\n"
            "  [4] List All Books\n"
            "  [0] Back",
            title="--- Staff Menu ---",
            border_style="yellow"
        ))

        choice = Prompt.ask("Choice", choices=["1", "2", "3", "4", "0"], default="1")

        if choice == '1':
            handle_add_book()
        elif choice == '2':
            handle_loan_approvals()
        elif choice == '3':
            handle_return_book()
        elif choice == '4':
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
    if not data.books:
        console.print("[yellow]No books in system.[/yellow]")
        return

    table = Table(title="Library Catalog")
    table.add_column("ID", style="dim")
    table.add_column("Title", style="magenta")
    table.add_column("Status", style="cyan")

    for b in data.books:
        status = "Available" if b.is_available else "[red]Borrowed[/red]"
        table.add_row(str(b.book_id), b.title, status)
    console.print(table)

def handle_loan_approvals():
    pending = [r for r in data.loans if r.status == LoanStatus.PENDING]
    
    if not pending:
        console.print("[green]No pending requests.[/green]")
        return

    table = Table(title="Pending Loans")
    table.add_column("Request ID", style="cyan")
    table.add_column("Book Title", style="magenta")
    table.add_column("Student", style="blue")
    
    for r in pending:
        # Helper to get names (inefficient lookup for display, but fine for CLI)
        b_title = next((b.title for b in data.books if b.book_id == r.book_id), "Unknown")
        s_name = next((s.username for s in data.students if s.student_id == r.student_id), "Unknown")
        table.add_row(str(r.request_id), b_title, s_name)
        
    console.print(table)

    req_id_str = Prompt.ask("Enter Request ID to APPROVE (or Enter to cancel)")
    if not req_id_str:
        return

    try:
        from uuid import UUID
        req_id = UUID(req_id_str)
        loan_service.approve_loan(req_id)
        console.print("[bold green]Loan Approved![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

def handle_return_book():
    # Find active loans
    active = [r for r in data.loans if r.status == LoanStatus.APPROVED]
    
    if not active:
        console.print("[green]No active loans to return.[/green]")
        return

    table = Table(title="Books Out on Loan")
    table.add_column("Request ID", style="cyan")
    table.add_column("Book", style="magenta")
    table.add_column("Borrowed By", style="blue")

    for r in active:
        b_title = next((b.title for b in data.books if b.book_id == r.book_id), "Unknown")
        s_name = next((s.username for s in data.students if s.student_id == r.student_id), "Unknown")
        table.add_row(str(r.request_id), b_title, s_name)
    console.print(table)
    
    req_id_str = Prompt.ask("Enter Request ID to RETURN (or Enter to cancel)")
    if not req_id_str:
        return

    try:
        from uuid import UUID
        req_id = UUID(req_id_str)
        loan_service.return_book(req_id)
        console.print("[bold green]Book Returned Successfully![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
