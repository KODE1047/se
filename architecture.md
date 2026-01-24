# architecture.md

# Project: University Library Management System (ULMS)
**Status:** Implementation - Iteration 2
**Last Updated:** 2026-01-23

## 1. Project Structure
(Unchanged from Iteration 1)

## 2. Tech Stack
(Unchanged)

## 3. Schema Map (Updated for Requirements)

### Users App
* **User:**
    * `role`: Enum [STUDENT, STAFF, ADMIN] (Renamed 'Librarian' to 'Staff')
    * `is_active`: Boolean (Used for Student Activation/Deactivation)

### Catalog App
* **Book:**
    * `created_by`: FK to User (Staff) - **REQUIRED for Staff Performance Reports**
    * `title`, `author`, `publication_year`, `isbn`
* **BookCopy:** (Kept for robust inventory management)

### Circulation App
* **BorrowRequest:** (Refactored from 'Loan')
    * `student`: FK to User
    * `book_copy`: FK to BookCopy
    * `start_date`: Date
    * `end_date`: Date
    * `status`: Enum [PENDING, APPROVED, REJECTED, RETURNED]
    * `approved_by`: FK to User (Staff) - **REQUIRED for Staff Performance Reports**
    * `approved_at`: Datetime

## 4. API Manifest (Mapped to Requirements)
* **Auth:**
    * `POST /register` (Student)
    * `POST /login`
* **Books:**
    * `GET /books` (Search: Title, Year, Author)
    * `POST /books` (Staff: Register Book)
* **Borrowing:**
    * `POST /borrow/request` (Student)
    * `PUT /borrow/requests/{id}/approve` (Staff - Date Logic Enforced)
    * `PUT /borrow/{id}/return` (Staff)
* **Stats:**
    * `GET /stats/summary` (Guest)
    * `GET /stats/employees` (Admin)

## 5. Decision Log
* **Borrowing Logic:** The requirement asks for a "Borrow Request" with a date range. We will implement a `BorrowRequest` model. When `approved`, it effectively becomes an active loan.
* **Performance Tracking:** To fulfill Requirement 4-2 (Staff Performance), we **must** add `created_by` to the `Book` model and `approved_by` to the `BorrowRequest` model. Without these foreign keys, generating performance reports is impossible.