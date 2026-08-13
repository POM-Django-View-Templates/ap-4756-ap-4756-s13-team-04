from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book
from author.models import Author
from authentication.models import CustomUser
from order.models import Order

def all_books(request):
    """Відображення всіх книг з можливістю фільтрації (для всіх користувачів)"""
    if not request.user.is_authenticated:
        messages.error(request, "Будь ласка, увійдіть в систему.")
        return redirect('home')

    # Отримуємо параметри фільтрації з GET-запиту
    title_query = request.GET.get('title', '').strip()
    author_query = request.GET.get('author', '').strip()

    # Початковий QuerySet усіх книг
    books = Book.objects.all()

    # Фільтрація за назвою книги (без урахування регістру)
    if title_query:
        books = books.filter(name__icontains=title_query)

    # Фільтрація за ID або Прізвищем автора
    if author_query:
        if author_query.isdigit():
            books = books.filter(authors__id=int(author_query))
        else:
            books = books.filter(authors__surname__icontains=author_query)

    # Унікалізуємо результати після filter по ManyToMany
    books = books.distinct()

    # Отримуємо список усіх авторів для випадаючого списку у фільтрі
    all_authors = Author.objects.all()

    context = {
        'books': books,
        'all_authors': all_authors,
        'title_query': title_query,
        'author_query': author_query,
    }
    return render(request, 'books/all_books.html', context)


def book_detail(request, book_id):
    """Перегляд конкретної книги (для всіх користувачів)"""
    if not request.user.is_authenticated:
        return redirect('home')
        
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def user_books(request, user_id):
    """Показ усіх книг, які зараз видані конкретному користувачу (тільки для бібліотекарів)"""
    # Захист доступу
    if not request.user.is_authenticated or request.user.role != 1:
        messages.error(request, "Access denied. For librarians only.")
        return redirect('home')

    # Отримуємо користувача, чиї книги хочемо переглянути
    target_user = get_object_or_404(CustomUser, id=user_id)
    
    # Вибираємо тільки ті замовлення користувача, де книги ще на руках (end_at відсутня)
    active_orders = Order.objects.filter(user=target_user, end_at__isnull=True)

    context = {
        'target_user': target_user,
        'orders': active_orders
    }
    return render(request, 'books/user_books.html', context)

