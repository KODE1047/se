import uuid
from dataclasses import dataclass, field
from uuid import UUID

@dataclass
class Book:
    """
    Data model representing a book in the library.

    Attributes:
        title (str): The title of the book.
        author (str): The author's name.
        publication_year (int): The year the book was published.
        book_id (UUID): Unique identifier, auto-generated.
        is_available (bool): Lending status (default: True).
    """
    title: str
    author: str
    publication_year: int
    book_id: UUID = field(default_factory=uuid.uuid4)
    is_available: bool = True