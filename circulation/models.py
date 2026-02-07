# circulation/models.py
import uuid
from django.db import models
from django.conf import settings
from catalog.models import BookCopy

class BorrowRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        RETURNED = 'RETURNED', 'Returned'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requests', on_delete=models.CASCADE)
    book_copy = models.ForeignKey(BookCopy, related_name='requests', on_delete=models.CASCADE)
    
    # Req 1-4: Specify start and end date
    start_date = models.DateField()
    end_date = models.DateField()
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Audit for Staff Performance (Req 4-2)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='approved_requests'
    )
    return_processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='processed_returns'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    actual_return_date = models.DateTimeField(null=True, blank=True)