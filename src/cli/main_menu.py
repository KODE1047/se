# /src/cli/main_menu.py
from rich.panel import Panel
from rich.prompt import Prompt
from cli.ui import console
from cli import student_menu
from cli import staff_menu
from cli import guest_menu
from cli import manager_menu

def run_main_menu():
    """
    Main application loop.
    """
    console.print("\nWelcome to the [bold cyan]University Library Management System[/]!")

    while True:
        console.print(Panel(
            "[bold]Select your user type:[/bold]\n\n"
            "  [1] Student\n"
            "  [2] Library Staff\n"
            "  [3] Guest\n"
            "  [4] System Manager\n"
            "  [0] Exit Application",
            title="--- Main Menu ---",
            border_style="blue"
        ))

        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "0"], default="1")

        if choice == '1':
            student_menu.run_student_menu()
        elif choice == '2':
            staff_menu.run_staff_menu()
        elif choice == '3':
            guest_menu.run_guest_menu()
        elif choice == '4':
            manager_menu.run_manager_menu()
        elif choice == '0':
            console.print("[bold]Exiting application. Goodbye.[/bold]")
            break
