from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('librarian_dashboard/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/author/delete/<int:author_id>/', views.delete_author, name='delete_author'),
]
