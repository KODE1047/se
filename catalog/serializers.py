# catalog/serializers.py
from rest_framework import serializers
from .models import Author, Book, BookCopy

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ['id', 'inventory_code', 'status']

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    # Nested serializer for read operations to show available copies
    copies_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'author', 'author_name', 'publication_year', 'copies_available']

    def get_copies_available(self, obj):
        return obj.copies.filter(status='AVAILABLE').count()