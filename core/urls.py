# /core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='core/login.html'), name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    
    # Student Views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.student_profile, name='profile'),
    path('loan/<uuid:book_id>/', views.request_loan, name='request_loan'),
    path('return/<uuid:loan_id>/', views.return_book, name='return_book'),
    
    # Staff/Manager Views
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('approve/<uuid:loan_id>/', views.approve_loan, name='approve_loan'),
    path('stats/', views.library_stats, name='library_stats'),
    
    # Guest
    path('guest/', views.guest_library, name='guest_library'),
]
