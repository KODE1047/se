# /architect.md

# 📚 University Library Management System - Architecture

This document outlines the software architecture, data models, and file structure.

## 1. Project Dependencies
* **`rich`**: For a "beautiful and readable" CLI.

## 2. Data Models

* **Student:** Represents a student user. (`src/models/student.py`)
    * `student_id`: (UUID) Unique identifier.
    * `username`: (str) Unique username.
    * `password_hash`: (str) Hashed password.
    * `is_active`: (bool) Status (default: `True`).

* **Book:** Represents a single book. (`src/models/book.py`)
    * `book_id`: (UUID) Unique identifier.
    * `title`: (str) Title.
    * `author`: (str) Author.
    * `publication_year`: (int) Year.
    * `is_available`: (bool) Lending status (default: `True`).

* **BorrowRequest:** Represents a transaction. (`src/models/borrow.py`)
    * `request_id`: (UUID) Unique identifier.
    * `student_id`: (UUID) Reference to Student.
    * `book_id`: (UUID) Reference to Book.
    * `status`: (Enum) `PENDING`, `APPROVED`, `RETURNED`, `REJECTED`.
    * `request_date`: (datetime) Timestamp.
    * `return_date`: (Optional[datetime]) Timestamp.

## 3. In-Memory Data Store
* **`src/data.py`**:
    * `students: List[Student]`
    * `books: List[Book]`
    * `loans: List[BorrowRequest]`

## 4. Services (Business Logic)

### 4.1. Student Service (`src/services/student_service.py`)
* `register_student(...) -> Student`
* `authenticate_student(...) -> Optional[Student]`

### 4.2. Book Service (`src/services/book_service.py`)
* `add_book(...) -> Book`

### 4.3. Search Service (`src/services/search_service.py`)
* `search_books(title, author, year) -> List[Book]`

### 4.4. Loan Service (`src/services/loan_service.py`)
* `request_loan(student_id, book_id) -> BorrowRequest`
* `approve_loan(request_id) -> None`

### 4.5. Report Service (`src/services/report_service.py`)
* `generate_student_report(student_id) -> Dict`
* `generate_library_stats() -> Dict`
