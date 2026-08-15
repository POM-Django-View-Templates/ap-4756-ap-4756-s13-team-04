import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from book.models import Book
from authentication.decorator import librarian_required

def orders_list_view(request):
    """Displaying orders: the librarian sees all, the user only sees their own."""
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to the system.")

        return redirect('login')

    if request.user.role == 1:
        orders = Order.objects.select_related('book', 'user').all().order_by('-created_at')
    else:
        orders = Order.objects.select_related('book').filter(user=request.user).order_by('-created_at')

    return render(request, 'order/orders_list.html', {'orders': orders})


def create_order_view(request, book_id):
    """Creating a book order by a reader through a custom method Order.create."""
    if not request.user.is_authenticated:

        return redirect('login')

    book = get_object_or_404(Book, id=book_id)
    plated_end_at = datetime.datetime.now() + datetime.timedelta(weeks=2)
    new_order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)
    if new_order:
        messages.success(request, f"Книгу «{book.name}» успішно замовлено!")
    else:
        messages.error(request, "Не вдалося замовити книгу. Можливо, вона закінчилася або вже заброньована.")

    return redirect('orders_list')


@librarian_required
def close_order_view(request, order_id):
    """Closing an order by a librarian via the order.update model method.""" 
    if request.method == 'POST':
        order = Order.get_by_id(order_id)
        if not order:
            messages.error(request, "Замовлення не знайдено.")

            return redirect('orders_list')
            
        if order.end_at is not None:
            messages.error(request, "Це замовлення вже було закрите.")
        else:
            order.update(end_at=datetime.datetime.now())
            messages.success(request, f"Замовлення №{order.id} успішно закрите.")

    return redirect('orders_list')
