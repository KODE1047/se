# circulation/views.py
from datetime import date, timedelta
from rest_framework import viewsets, permissions, status, decorators, exceptions
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import BorrowRequest
from .serializers import BorrowRequestSerializer

class BorrowRequestViewSet(viewsets.ModelViewSet):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Req 1-4: Student submit borrow request"""
        if request.user.role != 'STUDENT':
            raise exceptions.PermissionDenied("Only students can request books.")
        if not request.user.is_active:
             raise exceptions.PermissionDenied("Account is deactivated.")
        return super().create(request, *args, **kwargs)

    @decorators.action(detail=True, methods=['post'], permission_classes=[IsStaffOrAdmin])
    def approve(self, request, pk=None):
        """
        Req 3-5: Approve request. 
        Validation: Start date must be Today or Yesterday.
        """
        borrow_req = self.get_object()
        
        # Date Logic Validation
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        if borrow_req.start_date not in [today, yesterday]:
            return Response(
                {"error": "Cannot approve. Start date must be Today or Yesterday."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        borrow_req.status = 'APPROVED'
        borrow_req.approved_by = request.user
        borrow_req.book_copy.is_available = False # Lock the book
        borrow_req.book_copy.save()
        borrow_req.save()
        
        return Response({"status": "Approved"})

    @decorators.action(detail=True, methods=['post'], permission_classes=[IsStaffOrAdmin])
    def return_book(self, request, pk=None):
        """Req 3-8: Register return"""
        borrow_req = self.get_object()
        borrow_req.status = 'RETURNED'
        borrow_req.actual_return_date = timezone.now()
        borrow_req.return_processed_by = request.user # Track performance
        borrow_req.book_copy.is_available = True # Release book
        borrow_req.book_copy.save()
        borrow_req.save()
        return Response({"status": "Returned"})