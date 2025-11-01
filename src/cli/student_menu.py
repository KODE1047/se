# /src/cli/student_menu.py
import getpass
from src.services import student_service

def run_student_menu():
    """
    Displays the menu for Student users.
    """
    while True:
        print("\n--- Student Menu ---")
        print("1. Register (Req 1-1)")
        print("2. Login (Req 1-2) [Not Implemented]")
        print("3. List All Students (Testing)")
        print("0. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            handle_register_student()
        elif choice == '2':
            print("Login functionality is not yet implemented.")
        elif choice == '3':
            handle_list_students()
        elif choice == '0':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice, please try again.")

def handle_register_student():
    """Handles the UI for student registration."""
    print("\n[Student Registration]")
    username = input("Enter new username: ").strip()
    password = getpass.getpass("Enter new password: ").strip()
    
    if not username or not password:
        print("Error: Username and password cannot be empty.")
        return

    try:
        new_student = student_service.register_student(username, password)
        print(f"\nSuccess: Student '{new_student.username}' registered!")
        print(f"Your Student ID is: {new_student.student_id}")
    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def handle_list_students():
    """(For testing) Displays all students currently in the system."""
    from src.data import students # Import here to get the current list
    print("\n--- All Registered Students ---")
    if not students:
        print("No students registered yet.")
        return
        
    for i, student in enumerate(students):
        print(f"{i+1}. {student.username} (Active: {student.is_active})")
        print(f"   ID: {student.student_id}")
    print("-----------------------------")