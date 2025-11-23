# /src/main.py
from cli.main_menu import run_main_menu 
from cli.ui import console              

def main():
    """
    Main entry point for the University Library Management System.
    """
    try:
        run_main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Application exited manually. Goodbye![/bold yellow]")

if __name__ == "__main__":
    main()