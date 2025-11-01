# /src/cli/staff_menu.py
import getpass
from src.services import book_service

def run_staff_menu():
    """
    Displays the menu for Library Staff members.
    """
    while True:
        print("\n--- Library Staff Menu ---")
        print("1. Register New Book (Req 3-3)")
        print("2. List All Books (Testing)")
        print("0. Back to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            handle_add_book()
        elif choice == '2':
            handle_list_books()
        elif choice == '0':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice, please try again.")

def handle_add_book():
    """Handles the UI for adding a new book."""
    print("\n[Register New Book]")
    try:
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        year_str = input("Enter publication year: ").strip()
        
        if not title or not author or not year_str:
            print("Error: All fields are required.")
            return
            
        publication_year = int(year_str)
        
        new_book = book_service.add_book(
            title=title,
            author=author,
            publication_year=publication_year
        )
        print(f"\nSuccess: Book '{new_book.title}' added with ID: {new_book.book_id}")
        
    except ValueError:
        print("Error: Publication year must be a valid number.")
    except Exception as e:
        print(f"An error occurred: {e}")

def handle_list_books():
    """(For testing) Displays all books currently in the system."""
    from src.data import books  # Import here to get the current list
    print("\n--- All Registered Books ---")
    if not books:
        print("No books registered yet.")
        return
        
    for i, book in enumerate(books):
        print(f"{i+1}. {book.title} by {book.author} ({book.publication_year})")
        print(f"   ID: {book.book_id}")
        print(f"   Status: {'Available' if book.is_available else 'On Loan'}")
    print("----------------------------")