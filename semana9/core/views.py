from django.shortcuts import render, redirect
from .models import Livro
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/entrar")
def index(request):
    livros = Livro.objects.all()
    context = {
        'livro': livros
    }
    return render(request, 'index.html', context)

def livro(request, pk):
    livro = Livro.objects.get(id=pk)
    context = {
        'livro': livro
    }
    return render(request, 'livro.html', context)

def del_livro(request, pk):
    livro = Livro.objects.get(id=pk)
    livro.delete()
    return redirect('/')

def edit_livro(request, pk):
    
    if request.method == 'GET':
        livro = Livro.objects.get(id=pk)
        context = {
            "livro": livro
        }

        return render(request, 'edit_livro.html', context)
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        preco = request.POST.get('preco')

        if "," in preco:
            preco = preco.replace(",", ".")

        livro = Livro(
            title = titulo,
            price = preco,
        )

        livro.save()
        return redirect('/')
    
def cadastrar_livro(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'cad_livro.html')
        elif request.method == 'POST':
            titulo = request.POST.get('titulo')
            preco = request.POST.get('preco')

            livro = Livro(
                title = titulo,
                price = preco,
            )

            livro.save()
            return redirect('/')
    else:
        return redirect("/entrar")
    
def cad_user(request):
    if request.method == "GET":
        return render(request, 'cad_user.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username, email, password)
        user.save()
        return redirect("/entrar")

def entrar(request):
    if request.method == "GET":
        return render(request, "entrar.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")
        else:
            return HttpResponse("Falha ao tentar autenticar")
        
def sair(request):
    logout(request)
    return redirect("/entrar")