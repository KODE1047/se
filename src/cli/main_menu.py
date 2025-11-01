# /src/cli/main_menu.py
from src.cli import student_menu
from src.cli import staff_menu
# Import guest_menu and manager_menu will be added here later

def run_main_menu():
    """
    Main application loop.
    Displays the primary user selection menu and routes to sub-menus.
    """
    print("Welcome to the University Library Management System!")
    
    while True:
        print("\n--- Main Menu ---")
        print("Select your user type:")
        print("1. Student")
        print("2. Library Staff")
        print("3. Guest")
        print("4. System Manager")
        print("0. Exit Application")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            student_menu.run_student_menu()
        elif choice == '2':
            staff_menu.run_staff_menu()
        elif choice == '3':
            print("Guest menu not yet implemented.")
            # guest_menu.run_guest_menu()
        elif choice == '4':
            print("Manager menu not yet implemented.")
            # manager_menu.run_manager_menu()
        elif choice == '0':
            print("Exiting application. Goodbye.")
            break
        else:
            print("Invalid choice, please try again.")