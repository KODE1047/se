# /src/model/student.py


import hashlib
import uuid
from dataclasses import dataclass, field
from uuid import UUID

def hash_password(password: str) -> str:
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

@dataclass
class Student:
    """
    Data model representing a student user.
    
    Attributes:
        username (str): Unique username for login.
        password_hash (str): Hashed password.
        student_id (UUID): Unique identifier, auto-generated.
        is_active (bool): Status of the student (default: True, as per req 3-7).
    """
    username: str
    password_hash: str  # Store the hash, not the plain password
    student_id: UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True

    def check_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return self.password_hash == hash_password(password)

    @staticmethod
    def create_with_hashed_password(username: str, plain_password: str) -> 'Student':
        """
        Factory method to create a new Student instance with a hashed password.
        """
        password_hash = hash_password(plain_password)
        return Student(username=username, password_hash=password_hash)