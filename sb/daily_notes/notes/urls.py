from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.scrapbook, name='scrapbook'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('register/', views.register_page_view, name='register'),  # Add this line
    path('create/', views.create_note, name='create_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]