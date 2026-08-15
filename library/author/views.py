from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author
from authentication.decorator import librarian_required

FIRST_NAME_LENGTH = 20
LAST_NAME_LENGTH = 20
PATRONYMIC_LENGTH = 20

def home(request):
    """Home page."""

    return render(request, 'author/home.html')


@librarian_required
def librarian_dashboard(request):
    """
    Librarian dashboard for managing authors (Librarians only).
    Displays a list of all authors and handles creation of new records.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if not name or len(name) > FIRST_NAME_LENGTH:
            messages.error(request, "Ім'я є обов'язковим і не повинно перевищувати 20 символів.")
        elif not surname or len(surname) > LAST_NAME_LENGTH:
            messages.error(request, "Прізвище є обов'язковим і не повинно перевищувати 20 символів.")
        elif len(patronymic) > PATRONYMIC_LENGTH:
            messages.error(request, "По батькові не повинно перевищувати 20 символів.")
        else: 
            author = Author.create(name=name, surname=surname, patronymic=patronymic)
            if author:
                messages.success(request, f"Автора {surname} успішно додано!")

                return redirect('librarian_dashboard')
            else:
                messages.error(request, "Помилка бази даних під час створення автора.")

    authors = Author.objects.prefetch_related('books').all()
    context = {
        'authors': authors
    }

    return render(request, 'author/librarian_dashboard.html', context)


@librarian_required
def delete_author(request, author_id):
    """Delete an author, only if the request is POST and there are no linked books."""
    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        if author.books.exists():
            messages.error(request, f"Неможливо видалити автора {author.surname}, оскільки до нього прив'язані книги!")
        else:
            author.delete()
            messages.success(request, f"Автор {author.surname} успішно видалений!")
            
    return redirect('librarian_dashboard')
