# /src/services/search_service.py
from typing import List, Optional
from models.book import Book
import data as data

def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None
) -> List[Book]:
    """
    Searches for books matching ALL provided criteria.
    If all arguments are None, returns all books.
    """
    results = []
    for book in data.books:
        match = True
        if title and title.lower() not in book.title.lower():
            match = False
        if author and author.lower() != book.author.lower():
            match = False
        if year and year != book.publication_year:
            match = False
        
        if match:
            results.append(book)
            
    return results
