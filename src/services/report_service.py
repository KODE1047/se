# /src/services/report_service.py
from uuid import UUID
from datetime import datetime
from models.borrow import LoanStatus
import data as data

def generate_student_report(student_id: UUID) -> dict:
    """
    Returns stats for a specific student.
    """
    student_loans = [r for r in data.loans if r.student_id == student_id]
    
    total_loans = len(student_loans)
    # Unreturned: Approved but not Returned
    unreturned = len([r for r in student_loans if r.status == LoanStatus.APPROVED])
    
    # Overdue logic would go here (requires due date implementation)
    # For now, returning placeholder 0 as per basic requirements
    overdue = 0 

    return {
        "total_loans": total_loans,
        "unreturned_books": unreturned,
        "overdue_loans": overdue
    }

def generate_library_stats() -> dict:
    """
    Returns overall library stats.
    """
    # Calculate average loan duration for RETURNED books
    returned_loans = [r for r in data.loans if r.status == LoanStatus.RETURNED and r.return_date]
    
    if not returned_loans:
        avg_days = 0.0
    else:
        total_days = sum((r.return_date - r.request_date).days for r in returned_loans)
        avg_days = total_days / len(returned_loans)

    return {
        "average_loan_days": avg_days,
        "total_books": len(data.books),
        "total_students": len(data.students)
    }
