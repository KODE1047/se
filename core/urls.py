# /core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='core/login.html'), name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('loan/<uuid:book_id>/', views.request_loan, name='request_loan'),
    path('return/<uuid:loan_id>/', views.return_book, name='return_book'),
    path('guest/', views.guest_library, name='guest_library'), # <--- ADD THIS

]
