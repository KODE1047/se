# /tests/test_scenarios.py
import unittest
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4

# --- PATH CONFIGURATION ---
# Add the 'src' directory to sys.path so imports like 'models' work correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '../src')
sys.path.append(src_path)
# --------------------------

# Import Models
# Now we can import directly from 'models' and 'services' as if we were inside 'src'
from models.student import Student
from models.book import Book
from models.borrow import BorrowRequest, LoanStatus

# Import Services
import services.student_service as student_svc
import services.book_service as book_svc
import services.search_service as search_svc
import services.loan_service as loan_svc
import services.report_service as report_svc

# Import Data to clear it between tests
import data as db

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        """Reset the in-memory database before every test."""
        # We must clear the lists in the actual 'data' module
        db.students.clear()
        db.books.clear()
        db.loans.clear()

    # =========================================================================
    # Scenario 1: Authentication Service
    # =========================================================================

    def test_1_1_register_new_user(self):
        """1-1: Registering a new user with a unique username."""
        student = student_svc.register_student("unique_user", "pass123")
        self.assertIsInstance(student, Student)
        self.assertEqual(student.username, "unique_user")

    def test_1_2_register_duplicate_user(self):
        """1-2: Registering with a duplicate username."""
        student_svc.register_student("duplicate_user", "pass123")
        with self.assertRaises(ValueError):
            student_svc.register_student("duplicate_user", "pass456")

    def test_1_3_login_success(self):
        """1-3: Logging in with correct credentials."""
        student_svc.register_student("login_user", "correct_pass")
        result = student_svc.authenticate_student("login_user", "correct_pass")
        self.assertIsInstance(result, Student)
        self.assertEqual(result.username, "login_user")

    def test_1_4_login_wrong_password(self):
        """1-4: Logging in with incorrect password."""
        student_svc.register_student("wrong_pass_user", "correct_pass")
        result = student_svc.authenticate_student("wrong_pass_user", "wrong_pass")
        self.assertIsNone(result)

    def test_1_5_login_nonexistent_user(self):
        """1-5: Logging in with a username that does not exist."""
        result = student_svc.authenticate_student("ghost", "pass")
        self.assertIsNone(result)

    # =========================================================================
    # Scenario 2: Book Search Service
    # =========================================================================

    def test_2_1_search_by_title(self):
        """2-1: Searching by title only."""
        book_svc.add_book("Python 101", "Guido", 2000)
        book_svc.add_book("Java 101", "Gosling", 1995)
        
        results = search_svc.search_books(title="Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python 101")

    def test_2_2_search_by_author_and_year(self):
        """2-2: Searching by author and publication year."""
        book_svc.add_book("Book A", "Author X", 2020)
        book_svc.add_book("Book B", "Author X", 2021) # Wrong year
        
        results = search_svc.search_books(author="Author X", year=2020)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Book A")

    def test_2_3_search_all(self):
        """2-3: Searching without criteria."""
        book_svc.add_book("A", "B", 1)
        book_svc.add_book("C", "D", 2)
        
        results = search_svc.search_books()
        self.assertEqual(len(results), 2)

    def test_2_4_search_no_match(self):
        """2-4: Search matches no books."""
        book_svc.add_book("Real Book", "Author", 2020)
        results = search_svc.search_books(title="Fake Book")
        self.assertEqual(results, [])

    # =========================================================================
    # Scenario 3: Loan Management
    # =========================================================================

    def test_3_1_active_student_borrows_book(self):
        """3-1: Active student requests to borrow available book."""
        student = student_svc.register_student("active_std", "pass")
        book = book_svc.add_book("Avail Book", "Auth", 2022)
        
        req = loan_svc.request_loan(student.student_id, book.book_id)
        
        self.assertIsInstance(req, BorrowRequest)
        self.assertEqual(req.status, LoanStatus.PENDING)

    def test_3_2_inactive_student_borrows_book(self):
        """3-2: Inactive student attempts to borrow."""
        student = student_svc.register_student("inactive_std", "pass")
        student.is_active = False # Manually deactivate
        book = book_svc.add_book("Book", "Auth", 2022)
        
        with self.assertRaises(ValueError) as cm:
            loan_svc.request_loan(student.student_id, book.book_id)
        self.assertIn("not active", str(cm.exception))

    def test_3_3_borrow_unavailable_book(self):
        """3-3: Requesting a book that is already borrowed (unavailable)."""
        student = student_svc.register_student("s1", "p")
        book = book_svc.add_book("Rare Book", "Auth", 2022)
        book.is_available = False # Manually set unavailable
        
        with self.assertRaises(ValueError) as cm:
            loan_svc.request_loan(student.student_id, book.book_id)
        self.assertIn("unavailable", str(cm.exception))

    def test_3_4_approve_loan(self):
        """3-4: Approving a valid loan request."""
        student = student_svc.register_student("s1", "p")
        book = book_svc.add_book("Book", "Auth", 2022)
        req = loan_svc.request_loan(student.student_id, book.book_id)
        
        loan_svc.approve_loan(req.request_id)
        
        self.assertEqual(req.status, LoanStatus.APPROVED)
        self.assertFalse(book.is_available)

    def test_3_5_approve_already_approved(self):
        """3-5: Attempting to approve a request that is already approved."""
        student = student_svc.register_student("s1", "p")
        book = book_svc.add_book("Book", "Auth", 2022)
        req = loan_svc.request_loan(student.student_id, book.book_id)
        loan_svc.approve_loan(req.request_id)
        
        with self.assertRaises(ValueError) as cm:
            loan_svc.approve_loan(req.request_id)
        self.assertIn("Cannot approve", str(cm.exception))

    # =========================================================================
    # Scenario 4: Reporting Service
    # =========================================================================

    def test_4_1_student_report(self):
        """4-1: Generating a report for a student."""
        student = student_svc.register_student("s1", "p")
        book1 = book_svc.add_book("B1", "A", 2020)
        book2 = book_svc.add_book("B2", "A", 2020)
        
        # Req 1: Pending
        loan_svc.request_loan(student.student_id, book1.book_id)
        # Req 2: Approved
        req2 = loan_svc.request_loan(student.student_id, book2.book_id)
        loan_svc.approve_loan(req2.request_id)
        
        report = report_svc.generate_student_report(student.student_id)
        
        self.assertEqual(report['total_loans'], 2)
        self.assertEqual(report['unreturned_books'], 1) 

    def test_4_2_library_stats(self):
        """4-2: Calculating overall library statistics (Avg Loan Days)."""
        student = student_svc.register_student("s1", "p")
        book = book_svc.add_book("B1", "A", 2020)
        
        # Create a completed loan cycle
        req = loan_svc.request_loan(student.student_id, book.book_id)
        loan_svc.approve_loan(req.request_id)
        
        # Mock return
        req.status = LoanStatus.RETURNED
        req.request_date = datetime.now() - timedelta(days=5)
        req.return_date = datetime.now()
        
        stats = report_svc.generate_library_stats()
        self.assertAlmostEqual(stats['average_loan_days'], 5.0, delta=0.1)

if __name__ == '__main__':
    unittest.main()
