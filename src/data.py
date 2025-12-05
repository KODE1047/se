# /src/data.py
"""
In-memory data store.
"""
from typing import List
from models.student import Student
from models.book import Book
from models.borrow import BorrowRequest

# Global lists
students: List[Student] = []
books: List[Book] = []
loans: List[BorrowRequest] = []
