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
        messages.error(request, "Access denied. This page is for librarians only.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if not name or len(name) > 20:
            messages.error(request, "Name is required and must not exceed 20 characters.")
        elif not surname or len(surname) > 20:
            messages.error(request, "Surname is required and must not exceed 20 characters.")
        elif len(patronymic) > 20:
            messages.error(request, "Patronymic must not exceed 20 characters.")
        else: 
            author = Author.create(name=name, surname=surname, patronymic=patronymic)
            if author:
                messages.success(request, f"Author {surname} added successfully!")
                return redirect('librarian_dashboard')
            else:
                messages.error(request, "Error in database while creating author.")

    authors = Author.objects.all()
    librarians = CustomUser.objects.filter(role=1)

    context = {
        'authors': authors,
        'librarians': librarians
    }
    return render(request, 'librarian_dashboard.html', context)


def delete_author(request, author_id):
    """Deletes an author only if there is a secure POST request and no linked books."""
    if not request.user.is_authenticated or request.user.role != 1:
        messages.error(request, "Action available only for librarians.")
        return redirect('home')

    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        
        if author.books.exists():
            messages.error(request, f"Cannot delete author {author.surname}!")
        else:
            author.delete()
            messages.success(request, f"Author {author.surname} deleted successfully!")
            
    return redirect('librarian_dashboard')

def home(request):
    """Simple home page of the site."""
    return render(request, 'home.html')