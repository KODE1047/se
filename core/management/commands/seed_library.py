# /core/management/commands/seed_library.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Book

class Command(BaseCommand):
    help = 'Populates the library with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # 1. Create Books
        books_data = [
            ("Clean Code", "Robert C. Martin", 2008),
            ("The Pragmatic Programmer", "Andrew Hunt", 1999),
            ("Design Patterns", "Erich Gamma", 1994),
            ("Introduction to Algorithms", "Thomas H. Cormen", 2009),
            ("Refactoring", "Martin Fowler", 1999),
            ("The Hobbit", "J.R.R. Tolkien", 1937),
            ("Harry Potter", "J.K. Rowling", 1997),
        ]

        for title, author, year in books_data:
            book, created = Book.objects.get_or_create(
                title=title,
                defaults={'author': author, 'publication_year': year}
            )
            if created:
                self.stdout.write(f" - Added Book: {title}")

        # 2. Create Students
        students_data = [
            ("alice", "password123"),
            ("bob", "password123"),
        ]

        for username, password in students_data:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)
                self.stdout.write(f" - Added Student: {username}")

        self.stdout.write(self.style.SUCCESS("Successfully seeded library!"))
