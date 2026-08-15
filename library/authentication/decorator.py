from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def librarian_required(view_func):
    """A decorator that restricts access to the view to librarians only."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 1:
            messages.error(request, "Доступ обмежено. Сторінка лише для бібліотекарів.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view