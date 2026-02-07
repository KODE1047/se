# reports/views.py
from rest_framework import views, permissions, response
from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Avg, F
from catalog.models import Book
from circulation.models import BorrowRequest

User = get_user_model()

class GuestStatsView(views.APIView):
    """
    Req 2-1, 2-3: General Statistics for Guest
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = {
            "total_students": User.objects.filter(role='STUDENT').count(),
            "total_books": Book.objects.count(),
            "total_loans": BorrowRequest.objects.filter(status__in=['APPROVED', 'RETURNED']).count(),
            "currently_borrowed": BorrowRequest.objects.filter(status='APPROVED').count()
        }
        return response.Response(data)

class AdminStatsView(views.APIView):
    """
    Req 4-2, 4-3, 4-4: Advanced Reports
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Staff Performance
        staff_performance = User.objects.filter(role='STAFF').annotate(
            books_registered=Count('registered_books', distinct=True),
            loans_processed=Count('approved_requests', distinct=True),
            returns_processed=Count('processed_returns', distinct=True)
        ).values('email', 'books_registered', 'loans_processed', 'returns_processed')

        # Top Delayed Students (Req 4-4)
        # Logic: Count requests where return_date > end_date
        # Note: This is a simplified calculation for the "Greenfield" build
        delayed_students = User.objects.filter(role='STUDENT').annotate(
            late_returns=Count('requests', filter=Q(requests__actual_return_date__gt=F('requests__end_date')))
        ).order_by('-late_returns')[:10].values('email', 'late_returns')

        return response.Response({
            "staff_performance": staff_performance,
            "top_delayed_students": delayed_students
        })