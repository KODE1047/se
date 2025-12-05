# /core/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.author})"

class Loan(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('RETURNED', 'Returned'),
        ('REJECTED', 'Rejected'),
    ]
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    request_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.book.title}"
