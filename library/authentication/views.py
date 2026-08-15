from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser
from .decorator import librarian_required

FIRST_NAME_LENGTH = 20
LAST_NAME_LENGTH = 20
MIDDLE_NAME_LENGTH = 20
EMAIL_LENGTH = 100

def register_view(request):
    """Registration of a new user (visitor or librarian)."""
    if request.user.is_authenticated:

        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        role = request.POST.get('role', '0')

        error_msg = None

        if len(first_name) > FIRST_NAME_LENGTH or len(last_name) > LAST_NAME_LENGTH or len(middle_name) > MIDDLE_NAME_LENGTH:
            error_msg = "Ім'я, прізвище та по батькові не повинні перевищувати 20 символів."
        elif len(email) > EMAIL_LENGTH or '@' not in email:
            error_msg = "Некоректний формат Email або перевищено довжину (100 символів)."
        elif CustomUser.objects.filter(email=email).exists():
            error_msg = "Користувач з таким Email вже зареєстрований."

        if error_msg:
            messages.error(request, error_msg)
        else:
            try:
                CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    role=int(role),
                    is_active=True
                )
                messages.success(request, "Реєстрація пройшла успішно! Тепер ви можете увійти.")

                return redirect('login')
            except Exception:
                messages.error(request, "Виникла помилка під час створення акаунту.")

    return render(request, 'authentication/register.html')


def login_view(request):
    """Login."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f"Раді бачити вас знову, {user.first_name}!")

                return redirect('home')
            else:
                messages.error(request, "Ваш акаунт деактивовано.")
        else:
            messages.error(request, "Невірний Email або пароль.")

    return render(request, 'authentication/login.html')


def logout_view(request):
    """Logout."""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Ви успішно вийшли з системи.")

    return redirect('home')


@librarian_required
def all_users_view(request):
    """Showing information about all users"""
    users = CustomUser.objects.all()
    
    return render(request, 'authentication/all_users.html', {'users': users})


@librarian_required
def user_detail_view(request, user_id):
    """Showing details of a specific user by ID."""
    target_user = CustomUser.get_by_id(user_id)
    if not target_user:
        messages.error(request, "Користувача з таким ID не знайдено.")

        return redirect('all_users')

    return render(request, 'authentication/user_detail.html', {'target_user': target_user})
