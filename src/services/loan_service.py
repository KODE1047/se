# /src/services/loan_service.py
from uuid import UUID
from datetime import datetime
from models.borrow import BorrowRequest, LoanStatus
import data as data

def request_loan(student_id: UUID, book_id: UUID) -> BorrowRequest:
    """
    Creates a pending loan request.
    Raises ValueError if student inactive or book unavailable.
    """
    student = next((s for s in data.students if s.student_id == student_id), None)
    if not student:
        raise ValueError("Student not found.")
    if not student.is_active:
        raise ValueError("Student is not active.")

    book = next((b for b in data.books if b.book_id == book_id), None)
    if not book:
        raise ValueError("Book not found.")
    
    if not book.is_available:
         raise ValueError("Book is currently unavailable.")

    req = BorrowRequest(student_id=student_id, book_id=book_id)
    data.loans.append(req)
    return req

def approve_loan(request_id: UUID) -> None:
    """
    Approves a pending loan. Updates Book availability.
    """
    req = next((r for r in data.loans if r.request_id == request_id), None)
    if not req:
        raise ValueError("Request not found.")
    
    if req.status != LoanStatus.PENDING:
        raise ValueError(f"Cannot approve request with status: {req.status}")

    book = next((b for b in data.books if b.book_id == req.book_id), None)
    if book:
        if not book.is_available:
             raise ValueError("Book is no longer available.")
        book.is_available = False
    
    req.status = LoanStatus.APPROVED

def return_book(request_id: UUID) -> None:
    """
    Marks a loan as RETURNED and makes the book available again.
    """
    req = next((r for r in data.loans if r.request_id == request_id), None)
    if not req:
        raise ValueError("Request not found.")
    
    if req.status != LoanStatus.APPROVED:
        raise ValueError("Only APPROVED loans can be returned.")

    # 1. Update Request
    req.status = LoanStatus.RETURNED
    req.return_date = datetime.now()

    # 2. Update Book
    book = next((b for b in data.books if b.book_id == req.book_id), None)
    if book:
        book.is_available = True
