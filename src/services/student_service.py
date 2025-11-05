# /src/services/student_service.py
from models.student import Student  # MODIFIED
import data as data                 # MODIFIED

def register_student(username: str, password: str) -> Student:
    """
    Handles business logic for student registration.
    Checks for duplicate usernames.
    Creates and stores a new student.
    
    Raises:
        ValueError: If username already exists.
    """
    # 1. Check for duplicate username
    for student in data.students:
        if student.username == username:
            raise ValueError(f"Username '{username}' already exists.")
            
    # 2. Create new student (using the factory method from the model)
    new_student = Student.create_with_hashed_password(
        username=username,
        plain_password=password
    )
    
    # 3. Add to in-memory store
    data.students.append(new_student)
    
    return new_student