from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book
from author.models import Author
from authentication.models import CustomUser
from order.models import Order

def all_books(request):
    """Display all books with filterability (for all users)"""
    if not request.user.is_authenticated:
        messages.error(request, "Будь ласка, увійдіть в систему.")
        return redirect('home')

    title_query = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()

    books = Book.objects.all()
    if title_query:
        books = books.filter(name__icontains=title_query)

    if author_query:
        if author_query.isdigit():
            books = books.filter(authors__id=int(author_query))
        else:
            books = books.filter(authors__surname__icontains=author_query)

    books = books.distinct()

    all_authors = Author.objects.all()

    context = {
        'books': books,
        'all_authors': all_authors,
        'title_query': title_query,
        'author_query': author_query,
    }
    return render(request, 'book/all_books.html', context)


def book_detail(request, book_id):
    """View a specific book (for all users)"""
    if not request.user.is_authenticated:
        return redirect('home')
        
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book/book_detail.html', {'book': book})

def user_books(request, user_id):
    """Show all books currently issued to a specific user (for librarians only)"""
    if not request.user.is_authenticated or request.user.role != 1:
        messages.error(request, "Access denied. For librarians only.")
        return redirect('home')

    target_user = get_object_or_404(CustomUser, id=user_id)
    active_orders = Order.objects.filter(user=target_user, end_at__isnull=True)

    context = {
        'target_user': target_user,
        'orders': active_orders
    }
    return render(request, 'book/user_books.html', context)

