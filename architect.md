# /architect.md

# 📚 University Library Management System - Architecture

## 1. Project Dependencies
* **`rich`**: For a "beautiful and readable" CLI.

## 2. Data Models
* **Student** (`src/models/student.py`)
* **Book** (`src/models/book.py`)
* **BorrowRequest** (`src/models/borrow.py`)

## 3. In-Memory Data Store
* `src/data.py`

## 4. Services (Business Logic)
* **Student Service** (`src/services/student_service.py`): Register, Authenticate.
* **Book Service** (`src/services/book_service.py`): Add Book.
* **Search Service** (`src/services/search_service.py`): Search Logic.
* **Loan Service** (`src/services/loan_service.py`): Request/Approve Loans.
* **Report Service** (`src/services/report_service.py`): Aggregation.

## 5. CLI (Presentation Layer)
* **Main Menu** (`src/cli/main_menu.py`): Entry point.
* **Student Menu** (`src/cli/student_menu.py`): Registration, Login, Borrowing.
* **Staff Menu** (`src/cli/staff_menu.py`): Book Management, Loan Approval.
* **Guest Menu** (`src/cli/guest_menu.py`): Read-only access.
* **Manager Menu** (`src/cli/manager_menu.py`): Reporting.
