# 📚 University Library Management System - Architecture

This document outlines the software architecture, data models, and file structure.

## 1. Data Models

* **Student:** Represents a student user.
    * `student_id`: (UUID) Unique identifier.
    * `username`: (str) Unique username for login.
    * `password_hash`: (str) Hashed password for security.
    * `is_active`: (bool) Status of the student (default: `True`).
* **Book:** Represents a single book in the library.
    * `book_id`: (UUID) Unique identifier.
    * `title`: (str) The title of the book.
    * `author`: (str) The author's name.
    * `publication_year`: (int) The year the book was published.
    * `is_available`: (bool) Lending status (default: `True`).

## 2. Class Structures

### 2.1. Models

```python
# src/models/student.py
@dataclass
class Student:
    username: str
    password_hash: str
    student_id: UUID = field(default_factory=uuid4)
    is_active: bool = True

    def check_password(self, password: str) -> bool:
        ...

# Helper function in student.py
def hash_password(password: str) -> str:
    ...