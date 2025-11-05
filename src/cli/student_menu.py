# /src/cli/student_menu.py
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from services import student_service  # MODIFIED
from cli.ui import console            # MODIFIED
import data as data                   # MODIFIED

def run_student_menu():
    """
    Displays the menu for Student users.
    """
    while True:
        console.print(Panel(
            "[bold]What would you like to do?[/bold]\n\n"
            "  [1] Register (Req 1-1)\n"
            "  [2] Login (Req 1-2) [Not Implemented]\n"
            "  [3] List All Students (Testing)\n"
            "  [0] Back to Main Menu",
            title="--- Student Menu ---",
            border_style="green"
        ))
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "0"], default="1")
        
        if choice == '1':
            handle_register_student()
        elif choice == '2':
            console.print("[yellow]Login functionality is not yet implemented.[/yellow]")
        elif choice == '3':
            handle_list_students()
        elif choice == '0':
            console.print("[dim]Returning to Main Menu...[/dim]")
            break

def handle_register_student():
    """Handles the UI for student registration."""
    console.print("\n[bold]--- Student Registration ---[/bold]")
    username = Prompt.ask("Enter new username")
    password = Prompt.ask("Enter new password", password=True)
    
    if not username.strip() or not password.strip():
        console.print("[danger]Error: Username and password cannot be empty.[/danger]")
        return

    try:
        new_student = student_service.register_student(username, password)
        console.print(f"\n[bold green]Success: Student '{new_student.username}' registered![/bold green]")
        console.print(f"Your Student ID is: [cyan]{new_student.student_id}[/cyan]")
    except ValueError as e:
        console.print(f"\n[danger]Error: {e}[/danger]")
    except Exception as e:
        console.print(f"\n[danger]An unexpected error occurred: {e}[/danger]")

def handle_list_students():
    """(For testing) Displays all students currently in the system."""
    console.print("\n[bold]--- All Registered Students ---[/bold]")
    if not data.students:
        console.print("[yellow]No students registered yet.[/yellow]")
        return

    table = Table(title="Registered Students")
    table.add_column("Student ID", style="cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Status", justify="right", style="green")

    for student in data.students:
        status = "Active" if student.is_active else "Inactive"
        table.add_row(str(student.student_id), student.username, status)
        
    console.print(table)