from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.orders_list_view, name='orders_list'),
    path('orders/create/<int:book_id>/', views.create_order_view, name='create_order'),
    path('orders/close/<int:order_id>/', views.close_order_view, name='close_order'),
]
