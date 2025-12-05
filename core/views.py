# /core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Book, Loan

def signup(request):
    """Registers a new student."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def dashboard(request):
    """
    Main screen. 
    Shows 'Available Books' and 'My Loans'.
    """
    # 1. Available Books (Logic from Search Service)
    books = Book.objects.filter(is_available=True)
    
    # 2. My Loans (Logic from Report Service)
    my_loans = Loan.objects.filter(student=request.user).order_by('-request_date')

    return render(request, 'core/dashboard.html', {
        'books': books,
        'my_loans': my_loans
    })

@login_required
def request_loan(request, book_id):
    """Logic to borrow a book."""
    book = get_object_or_404(Book, pk=book_id)
    
    if book.is_available:
        # Create Loan
        Loan.objects.create(student=request.user, book=book, status='APPROVED')
        # Update Book
        book.is_available = False
        book.save()
        messages.success(request, f"You borrowed '{book.title}'")
    else:
        messages.error(request, "Book is not available.")
    
    return redirect('dashboard')

@login_required
def return_book(request, loan_id):
    """Logic to return a book."""
    loan = get_object_or_404(Loan, pk=loan_id, student=request.user)
    
    if loan.status == 'APPROVED':
        loan.status = 'RETURNED'
        loan.return_date = timezone.now()
        loan.save()
        
        # Make book available again
        loan.book.is_available = True
        loan.book.save()
        messages.success(request, "Book returned successfully.")
        
    return redirect('dashboard')
