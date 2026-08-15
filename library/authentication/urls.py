from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.all_users_view, name='all_users'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
]