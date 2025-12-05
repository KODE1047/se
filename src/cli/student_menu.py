# /src/cli/student_menu.py
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from cli.ui import console
from services import student_service, loan_service, report_service, search_service
import data

def run_student_menu():
    """
    Displays the public menu for Student users.
    """
    while True:
        console.print(Panel(
            "[bold]Student Portal[/bold]\n\n"
            "  [1] Register\n"
            "  [2] Login\n"
            "  [0] Back to Main Menu",
            title="--- Student Menu ---",
            border_style="green"
        ))
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "0"], default="1")

        if choice == '1':
            handle_register_student()
        elif choice == '2':
            handle_login()
        elif choice == '0':
            break

def handle_register_student():
    console.print("\n[bold]--- Registration ---[/bold]")
    username = Prompt.ask("Choose username")
    password = Prompt.ask("Choose password", password=True)
    
    try:
        new_student = student_service.register_student(username, password)
        console.print(f"[bold green]Success![/bold green] ID: {new_student.student_id}")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

def handle_login():
    console.print("\n[bold]--- Login ---[/bold]")
    username = Prompt.ask("Username")
    password = Prompt.ask("Password", password=True)

    student = student_service.authenticate_student(username, password)
    
    if student:
        if not student.is_active:
            console.print("[red]Account is inactive. Contact manager.[/red]")
            return
        console.print(f"[green]Welcome back, {student.username}![/green]")
        run_logged_in_menu(student)
    else:
        console.print("[bold red]Invalid credentials.[/bold red]")

def run_logged_in_menu(student):
    """
    Menu accessible only AFTER login.
    """
    while True:
        console.print(Panel(
            f"User: [cyan]{student.username}[/cyan]\n\n"
            "  [1] Search & Borrow Books\n"
            "  [2] My Profile (Reports)\n"
            "  [0] Logout",
            title="--- Student Dashboard ---",
            border_style="green"
        ))
        choice = Prompt.ask("Choice", choices=["1", "2", "0"])

        if choice == '1':
            handle_borrow_flow(student)
        elif choice == '2':
            handle_profile(student)
        elif choice == '0':
            break

def handle_borrow_flow(student):
    # reuse logic from guest menu or similar, but with 'Borrow' option
    console.print("\n[bold]Search for a book to borrow:[/bold]")
    title = Prompt.ask("Title search").strip() or None
    results = search_service.search_books(title=title)
    
    if not results:
        console.print("[yellow]No books found.[/yellow]")
        return

    # Display
    table = Table()
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Available", style="yellow")
    
    for b in results:
        table.add_row(str(b.book_id), b.title, "Yes" if b.is_available else "No")
    console.print(table)

    # Action
    book_id_str = Prompt.ask("Enter Book ID to borrow (or press Enter to cancel)")
    if not book_id_str:
        return

    try:
        # Convert string to UUID object
        from uuid import UUID
        book_uuid = UUID(book_id_str)
        
        req = loan_service.request_loan(student.student_id, book_uuid)
        console.print(f"[bold green]Request Submitted![/bold green] Request ID: {req.request_id}")
        console.print("Status: [yellow]PENDING[/yellow] (Wait for Staff approval)")
    except ValueError as e: # Handles invalid UUID format or Logic errors
        console.print(f"[red]Error:[/red] {e}")
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/red] {e}")

def handle_profile(student):
    report = report_service.generate_student_report(student.student_id)
    console.print(Panel(
        f"Total Loans: {report['total_loans']}\n"
        f"Books Currently Held: {report['unreturned_books']}\n"
        f"Overdue: {report['overdue_loans']}",
        title="My Profile"
    ))
