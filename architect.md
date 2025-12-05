# architect.md

# 📚 University Library PWA - Architecture

**Version:** 2.0 (Web/PWA)
**Framework:** Django 5.x
**Frontend:** Bootstrap 5 + Django Templates
**Database:** SQLite (Dev) / PostgreSQL (Prod)

---

## 1. Project Structure

```text
/ (Root)
├── manage.py                # CLI Entry Point
├── db.sqlite3               # Database
├── requirements.txt         # Dependencies
├── architect.md             # This File
│
├── django_pwa/              # Project Configuration
│   ├── settings.py          # Installed Apps, PWA Config
│   ├── urls.py              # Root Routing
│   └── wsgi.py              # Server Entry
│
├── core/                    # Main Application
│   ├── models.py            # Database Schema
│   ├── views.py             # Business Logic (Controllers)
│   ├── urls.py              # App Routing
│   ├── admin.py             # Internal Management
│   ├── management/          # Custom Commands (Seeding)
│   └── templates/           # HTML Views
│
└── static/                  # PWA Assets
    ├── css/                 # Custom Styling
    ├── js/                  # Service Worker
    └── images/              # App Icons
```

---

## 2. Data Models (`core/models.py`)

We utilize the Django ORM (Object-Relational Mapping) to translate Python classes to SQL tables.

### 2.1 User (Django Built-in)
*   **Table:** `auth_user`
*   **Usage:** Handles Authentication, Password Hashing, and Groups (Staff/Student).
*   **Key Fields:** `username`, `password` (hashed), `is_active`, `is_staff`.

### 2.2 Book
*   **Table:** `core_book`
*   **PK:** `book_id` (UUID)
*   **Fields:**
    *   `title` (Char)
    *   `author` (Char)
    *   `publication_year` (Int)
    *   `is_available` (Bool) - Default: `True`

### 2.3 Loan
*   **Table:** `core_loan`
*   **PK:** `request_id` (UUID)
*   **Foreign Keys:** `student` (User), `book` (Book)
*   **Fields:**
    *   `status` (Enum): `PENDING`, `APPROVED`, `RETURNED`, `REJECTED`
    *   `request_date` (DateTime) - Auto-set on creation.
    *   `return_date` (DateTime) - Nullable.

---

## 3. Feature Implementation (Scenario Mapping)

This section maps the Requirements to the actual Code Logic.

### Scenario 1: Authentication Service
*   **1-1 (Register Unique):** Handled by `views.signup`. Uses `UserCreationForm`. Returns Success.
*   **1-2 (Register Duplicate):** Handled by `UserCreationForm` validation. Returns Error Message.
*   **1-3 (Login Success):** Handled by `auth_views.LoginView`. Redirects to Dashboard.
*   **1-4/1-5 (Login Fail):** Handled by `auth_views.LoginView`. Re-renders login with error.

### Scenario 2: Book Search Service
*   **Location:** `views.dashboard`
*   **Logic:**
    *   **2-1 (Title):** `Book.objects.filter(title__icontains=q)`
    *   **2-2 (Author/Year):** Chained filters `filter(author=...).filter(year=...)`
    *   **2-3 (No Criteria):** Returns `Book.objects.all()`
    *   **2-4 (No Match):** Template displays "No books match".

### Scenario 3: Loan Management
*   **3-1 (Request):** `views.request_loan`. Creates `Loan(status='PENDING')`.
*   **3-2 (Inactive Student):** Guard clause `if not request.user.is_active`.
*   **3-3 (Unavailable Book):** Guard clause `if not book.is_available`.
*   **3-4 (Staff Approve):** `views.approve_loan`. Sets `status='APPROVED'` and `book.is_available=False`.
*   **3-5 (Double Approve):** Guard clause `if loan.status != 'PENDING'`.

### Scenario 4: Reporting Service
*   **4-1 (Student Profile):** `views.student_profile`.
    *   Calculates: `total_loans`, `unreturned` (Approved status), `overdue` (Date diff > 14 days).
*   **4-2 (Library Stats):** `views.library_stats`.
    *   Calculates: `Avg(return_date - request_date)` for Returned loans.

---

## 4. PWA Configuration

### Manifest (`settings.py`)
*   **Name:** UniLibrary
*   **Theme Color:** `#0d6efd` (Bootstrap Primary)
*   **Display:** Standalone (Native App feel)

### Service Worker (`static/js/serviceworker.js`)
*   **Strategy:** Cache First for Static Assets, Network First for Data.
*   **Cached Routes:** `/`, `/dashboard/`, `/guest/`, Bootstrap CDN.
*   **Offline Capabilities:** Users can view the dashboard UI even without internet (data may be stale).

---

## 5. URL Routing Table

| URL Pattern | View Function | Access Level |
| :--- | :--- | :--- |
| `/` | `LoginView` | Public |
| `/signup/` | `signup` | Public |
| `/guest/` | `guest_library` | Public |
| `/dashboard/` | `dashboard` | Student (Logged In) |
| `/profile/` | `student_profile` | Student (Logged In) |
| `/loan/<uuid>/` | `request_loan` | Student (Active) |
| `/return/<uuid>/` | `return_book` | Student/Staff |
| `/staff/` | `staff_dashboard` | Staff Only |
| `/approve/<uuid>/` | `approve_loan` | Staff Only |
| `/stats/` | `library_stats` | Staff Only |