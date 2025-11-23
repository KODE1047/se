# /src/data.py
"""
In-memory data store.
"""
from typing import List
from models.student import Student  
from models.book import Book        

# Global lists to store data
students: List[Student] = [
    Student.create_with_hashed_password("alice", "password123"),
    Student.create_with_hashed_password("bob", "securepass"),
    Student.create_with_hashed_password("charlie", "mypassword"),
    Student.create_with_hashed_password("diana", "librarypass")
]

books: List[Book] = [
    Book("The Great Gatsby", "F. Scott Fitzgerald", 1925),
    Book("To Kill a Mockingbird", "Harper Lee", 1960),
    Book("1984", "George Orwell", 1949),
    Book("Pride and Prejudice", "Jane Austen", 1813),
    Book("The Catcher in the Rye", "J.D. Salinger", 1951)
]