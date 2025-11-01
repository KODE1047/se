# /src/services/book_service.py
from src.models.book import Book
import src.data as data

def add_book(title: str, author: str, publication_year: int) -> Book:
    """
    Handles business logic for adding a new book (Req 3-3).
    Creates and stores a new book.
    """
    
    # 1. Create new book
    new_book = Book(
        title=title,
        author=author,
        publication_year=publication_year
    )
    
    # 2. Add to in-memory store
    data.books.append(new_book)
    
    return new_book