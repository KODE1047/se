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
    # 1. Validate Student
    student = next((s for s in data.students if s.student_id == student_id), None)
    if not student:
        raise ValueError("Student not found.")
    if not student.is_active:
        raise ValueError("Student is not active.")

    # 2. Validate Book
    book = next((b for b in data.books if b.book_id == book_id), None)
    if not book:
        raise ValueError("Book not found.")
    
    # Check if book is already borrowed/approved in active loans
    # (Assuming 'is_available' flag on Book is the source of truth for current availability)
    if not book.is_available:
         raise ValueError("Book is currently unavailable.")

    # 3. Create Request
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

    # Find book to update status
    book = next((b for b in data.books if b.book_id == req.book_id), None)
    if book:
        if not book.is_available:
             raise ValueError("Book is no longer available.")
        book.is_available = False
    
    req.status = LoanStatus.APPROVED
