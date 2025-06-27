from django.urls import path
from .views import index, livro, cadastrar_livro, del_livro

urlpatterns = [
    path('', index),
    path('Livro/<int:pk>', livro, name='Livro'),
    path('del_livro/<int:pk>', del_livro, name='deletar_livro_url'),
    path('cad_livro', cadastrar_livro, name='cadastrar_livro_url')
]