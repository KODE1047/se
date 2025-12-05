# /src/cli/manager_menu.py
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from cli.ui import console
from services import report_service
import data

def run_manager_menu():
    """
    Displays the menu for System Managers.
    """
    while True:
        console.print(Panel(
            "[bold]System Management[/bold]\n\n"
            "  [1] View Library Statistics\n"
            "  [2] View All Students\n"
            "  [0] Back to Main Menu",
            title="--- Manager Menu ---",
            border_style="red"
        ))

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "0"], default="1")

        if choice == '1':
            handle_stats()
        elif choice == '2':
            handle_all_students()
        elif choice == '0':
            break

def handle_stats():
    """Displays global library stats."""
    stats = report_service.generate_library_stats()
    
    console.print("\n[bold underline]Library Statistics[/bold underline]")
    console.print(f"Total Books:    [cyan]{stats['total_books']}[/cyan]")
    console.print(f"Total Students: [cyan]{stats['total_students']}[/cyan]")
    console.print(f"Avg Loan Time:  [green]{stats['average_loan_days']:.2f} days[/green]")

def handle_all_students():
    """Lists all students with their specific report data."""
    if not data.students:
        console.print("[yellow]No students registered.[/yellow]")
        return

    table = Table(title="Student Reports")
    table.add_column("Username", style="magenta")
    table.add_column("Total Loans", justify="right")
    table.add_column("Unreturned", justify="right", style="red")

    for student in data.students:
        report = report_service.generate_student_report(student.student_id)
        table.add_row(
            student.username,
            str(report['total_loans']),
            str(report['unreturned_books'])
        )
    console.print(table)
