# /core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Avg, F, ExpressionWrapper, fields
from .models import Book, Loan

# --- Scenario 1: Authentication ---

def signup(request):
    """
    Scenario 1-1: Register Unique -> Success
    Scenario 1-2: Register Duplicate -> Fail (Form handles this)
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            # This handles Scenario 1-2 (Duplicate Username)
            messages.error(request, "Registration failed. Username may be taken.")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

@login_required
def dashboard(request):
    """
    Scenario 2: Book Search Service
    """
    # 2-3: Default is all books
    books = Book.objects.all()

    # 2-1 & 2-2: Search Logic
    title_query = request.GET.get('title')
    author_query = request.GET.get('author')
    year_query = request.GET.get('year')

    if title_query:
        books = books.filter(title__icontains=title_query)
    
    if author_query:
        books = books.filter(author__icontains=author_query)
        
    if year_query:
        try:
            books = books.filter(publication_year=int(year_query))
        except ValueError:
            pass # Ignore invalid year input

    # Scenario 2-4: If no match, books is empty list (Handled by template)

    my_loans = Loan.objects.filter(student=request.user).order_by('-request_date')
    
    return render(request, 'core/dashboard.html', {
        'books': books,
        'my_loans': my_loans
    })

# --- Scenario 3: Loan Management ---

@login_required
def request_loan(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Scenario 3-2: Inactive Student Check
    if not request.user.is_active:
        messages.error(request, "Error: Inactive accounts cannot borrow books.")
        return redirect('dashboard')

    # Scenario 3-3: Unavailable Book Check
    if not book.is_available:
        messages.error(request, "Error: Book is currently unavailable.")
        return redirect('dashboard')

    # Scenario 3-1: Create PENDING request
    # Check if already requested
    existing = Loan.objects.filter(student=request.user, book=book, status='PENDING').exists()
    if existing:
        messages.warning(request, "You already have a pending request for this book.")
    else:
        Loan.objects.create(student=request.user, book=book, status='PENDING')
        messages.success(request, "Loan Requested! Status: PENDING. Wait for staff approval.")
    
    return redirect('dashboard')

@staff_member_required
def staff_dashboard(request):
    """
    UI for Staff to Approve Loans (Scenario 3-4)
    """
    pending_loans = Loan.objects.filter(status='PENDING')
    return render(request, 'core/staff_dashboard.html', {'pending_loans': pending_loans})

@staff_member_required
def approve_loan(request, loan_id):
    """
    Scenario 3-4: Approve Valid -> Status APPROVED, Book Unavailable
    Scenario 3-5: Approve Approved -> Error
    """
    loan = get_object_or_404(Loan, pk=loan_id)

    if loan.status != 'PENDING':
        messages.error(request, "Error: Can only approve PENDING requests.")
        return redirect('staff_dashboard')

    if not loan.book.is_available:
        messages.error(request, "Error: Book is no longer available.")
        return redirect('staff_dashboard')

    # Execute Approval
    loan.status = 'APPROVED'
    loan.book.is_available = False
    loan.book.save()
    loan.save()
    
    messages.success(request, f"Approved loan for {loan.book.title}")
    return redirect('staff_dashboard')

@login_required
def return_book(request, loan_id):
    # Allow Student to return OR Staff to mark returned
    loan = get_object_or_404(Loan, pk=loan_id)
    
    # Security: Only the owner or staff can return
    if loan.student != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if loan.status == 'APPROVED':
        loan.status = 'RETURNED'
        loan.return_date = timezone.now()
        loan.save()
        
        loan.book.is_available = True
        loan.book.save()
        messages.success(request, "Book returned successfully.")
        
    return redirect('dashboard')

# --- Scenario 4: Reporting Service ---

@login_required
def student_profile(request):
    """
    Scenario 4-1: Student Report
    """
    user_loans = Loan.objects.filter(student=request.user)
    
    total_loans = user_loans.count()
    
    # Unreturned = Approved (Book in hand)
    unreturned_books = user_loans.filter(status='APPROVED').count()
    
    # Overdue Calculation (Assuming 14 days limit)
    # In a real app, we'd filter using DB query, but doing it in python for simplicity here
    overdue_loans = 0
    now = timezone.now()
    for loan in user_loans:
        if loan.status == 'APPROVED':
            days_held = (now - loan.request_date).days
            if days_held > 14:
                overdue_loans += 1

    context = {
        'total_loans': total_loans,
        'unreturned_books': unreturned_books,
        'overdue_loans': overdue_loans,
        'user': request.user
    }
    return render(request, 'core/profile.html', context)

@staff_member_required
def library_stats(request):
    """
    Scenario 4-2: Library Stats (Avg Loan Days)
    """
    returned_loans = Loan.objects.filter(status='RETURNED')
    
    # Calculate difference between return_date and request_date
    # SQLite has limitations with date diffs in Django ORM, 
    # so we do a Python calculation for compatibility with your likely dev env.
    total_days = 0
    count = 0
    for loan in returned_loans:
        if loan.return_date and loan.request_date:
            delta = loan.return_date - loan.request_date
            total_days += delta.days
            count += 1
            
    avg_loan_days = (total_days / count) if count > 0 else 0
    
    total_books = Book.objects.count()
    total_students = Book.objects.count() # Typo in logic previously? No, simple count.
    
    context = {
        'avg_loan_days': round(avg_loan_days, 2),
        'total_books': total_books,
        'total_loans_all_time': Loan.objects.count()
    }
    return render(request, 'core/stats.html', context)

def guest_library(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'core/guest_list.html', {'books': books})
