# /architect.md
# 📚 University Library Management System - Architecture

This document outlines the software architecture, data models, and file structure.

## 1. Data Models

* **Student:** Represents a student user. (`src/models/student.py`)
    * `student_id`: (UUID) Unique identifier.
    * `username`: (str) Unique username for login.
    * `password_hash`: (str) Hashed password for security.
    * `is_active`: (bool) Status of the student (default: `True`).
* **Book:** Represents a single book in the library. (`src/models/book.py`)
    * `book_id`: (UUID) Unique identifier.
    * `title`: (str) The title of the book.
    * `author`: (str) The author's name.
    * `publication_year`: (int) The year the book was published.
    * `is_available`: (bool) Lending status (default: `True`).

## 2. In-Memory Data Store

* **`src/data.py`**: Holds the runtime data.
    * `students: List[Student] = []`
    * `books: List[Book] = []`

## 3. Services (Business Logic)

### 3.1. Student Service (`src/services/student_service.py`)

```python
def register_student(username: str, password: str) -> Student:
    """
    Handles business logic for student registration.
    Checks for duplicate usernames.
    Creates and stores a new student.
    Raises:
        ValueError: If username already exists.
    """
    ...