from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Author
from authentication.models import CustomUser

def librarian_dashboard(request):
    """
    Librarian Panel.
    Displays information about all authors, librarians, and handles author creation.
    """
    if not request.user.is_authenticated or request.user.role != 1:
        messages.error(request, "Доступ обмежено. Ця сторінка призначена лише для бібліотекарів.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if not name or len(name) > 20:
            messages.error(request, "Ім'я є обов'язковим і не повинно перевищувати 20 символів.")
        elif not surname or len(surname) > 20:
            messages.error(request, "Прізвище є обов'язковим і не повинно перевищувати 20 символів.")
        elif len(patronymic) > 20:
            messages.error(request, "По-батькові не повинно перевищувати 20 символів.")
        else: 
            author = Author.create(name=name, surname=surname, patronymic=patronymic)
            if author:
                messages.success(request, f"Автор {surname} доданий успішно!")
                return redirect('librarian_dashboard')
            else:
                messages.error(request, "Помилка в базі даних під час створення автора.")

    authors = Author.objects.all()
    librarians = CustomUser.objects.filter(role=1)

    context = {
        'authors': authors,
        'librarians': librarians
    }
    return render(request, 'author/librarian_dashboard.html', context)


def delete_author(request, author_id):
    """Deletes an author only if there is a secure POST request and no linked books."""
    if not request.user.is_authenticated or request.user.role != 1:
        messages.error(request, "Дія доступна лише для бібліотекарів.")
        return redirect('home')

    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        
        if author.books.exists():
            messages.error(request, f"Неможливо видалити автора {author.surname}!")
        else:
            author.delete()
            messages.success(request, f"Автор {author.surname} успішно видалений!")
            
    return redirect('librarian_dashboard')

def home(request):
    """Simple home page of the site."""
    return render(request, 'author/home.html')