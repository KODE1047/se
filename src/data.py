# /src/data.py
"""
In-memory data store with SEED DATA.
"""
from typing import List
from models.student import Student
from models.book import Book
from models.borrow import BorrowRequest
import uuid

# Global lists
students: List[Student] = []
books: List[Book] = []
loans: List[BorrowRequest] = []

def initialize_data():
    """Populates the system with initial data for testing."""
    # 1. Seed Students
    # Password for all is 'password123'
    s1 = Student.create_with_hashed_password("alice", "password123")
    s2 = Student.create_with_hashed_password("bob", "password123")
    students.extend([s1, s2])

    # 2. Seed Books
    b1 = Book("Clean Code", "Robert C. Martin", 2008)
    b2 = Book("The Pragmatic Programmer", "Andrew Hunt", 1999)
    b3 = Book("Design Patterns", "Erich Gamma", 1994)
    b4 = Book("Introduction to Algorithms", "Thomas H. Cormen", 2009)
    b5 = Book("Refactoring", "Martin Fowler", 1999)
    books.extend([b1, b2, b3, b4, b5])

# Run initialization immediately on import
initialize_data()
