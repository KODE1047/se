# /src/services/student_service.py
from typing import Optional
from models.student import Student
import data as data

def register_student(username: str, password: str) -> Student:
    """
    Registers a new student.
    Raises ValueError if username exists.
    """
    for student in data.students:
        if student.username == username:
            raise ValueError(f"Username '{username}' already exists.")

    new_student = Student.create_with_hashed_password(username, password)
    data.students.append(new_student)
    return new_student

def authenticate_student(username: str, password: str) -> Optional[Student]:
    """
    Authenticates a student.
    Returns the Student object if successful, None otherwise.
    """
    for student in data.students:
        if student.username == username and student.check_password(password):
            return student
    return None
