# /src/models/borrow.py
import uuid
from dataclasses import dataclass, field
from uuid import UUID
from enum import Enum, auto
from datetime import datetime
from typing import Optional

class LoanStatus(Enum):
    PENDING = auto()
    APPROVED = auto()
    RETURNED = auto()
    REJECTED = auto()

@dataclass
class BorrowRequest:
    student_id: UUID
    book_id: UUID
    status: LoanStatus = LoanStatus.PENDING
    request_id: UUID = field(default_factory=uuid.uuid4)
    request_date: datetime = field(default_factory=datetime.now)
    return_date: Optional[datetime] = None
