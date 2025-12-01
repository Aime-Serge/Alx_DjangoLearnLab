import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')
django.setup()

from relationship_app.models import Author
from relationship_app.models import Book
from relationship_app.models import Library
from relationship_app.models import Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author using Book.objects.filter."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name}: {[book.title for book in books]}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' does not exist.")


def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in books]}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' does not exist.")


def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library using Librarian.objects.get(library=...)."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  
        print(f"Librarian for {library_name}: {librarian.name}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' does not exist.")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")


if __name__ == '__main__':
    query_books_by_author("J.K. Rowling")
    list_books_in_library("Central Library")
    retrieve_librarian_for_library("Central Library")