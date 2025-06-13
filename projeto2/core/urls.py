from django.urls import path
from .views import index, livro, delete

urlpatterns = [
    path("", index),
    path("Livro/<int:pk>", livro, name="Livro"),
    path("Livro/<int:pk>/delete", delete, name="Delete")
]