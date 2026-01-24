# catalog/views.py
from rest_framework import viewsets, permissions, filters
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    Req 1-3: Search Books (Title, Year, Author)
    Req 3-3: Register Books (Staff)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author', 'publication_year']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Req 3-3, 3-4: Only Staff can manage books
            return [permissions.IsAuthenticated(), IsStaffOrAdmin()]
        # Req 2-2: Guests can Search
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # Automatically set created_by for performance tracking
        serializer.save(created_by=self.request.user)

# Custom Permission
class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['STAFF', 'ADMIN']