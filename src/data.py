# /src/data.py
"""
In-memory data store.

This module acts as a temporary, in-memory database for the application's
runtime. All data will be lost when the application exits.
"""
from typing import List
from src.models.student import Student
from src.models.book import Book

# Global lists to store data
students: List[Student] = []
books: List[Book] = []