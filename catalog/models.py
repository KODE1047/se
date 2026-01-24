# catalog/models.py
import uuid
from django.db import models
from django.conf import settings

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255) # Simplified as per prompt 'Author' search
    publication_year = models.IntegerField()
    
    # Req 4-2: Track who registered the book for performance reports
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='registered_books'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class BookCopy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, related_name='copies', on_delete=models.CASCADE)
    inventory_code = models.CharField(max_length=50, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book.title} ({self.inventory_code})"