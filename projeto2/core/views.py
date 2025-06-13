from django.shortcuts import render
from .models import Livro

def index(request):
    livros = Livro.objects.all()
    context = {
        'livro': livros
    }

    return render(request, "index.html", context)

def livro(request, pk):
    livro = Livro.objects.get(id=pk)
    context = {
        'livro': livro
    }
    return render(request, 'livro.html', context)

def delete(request, pk):
    if request.method == "POST":
        livro = Livro.objects.get(id=pk)
        livro.delete()
    
    return render(request, "index.html")
