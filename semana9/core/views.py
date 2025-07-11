from django.shortcuts import render, redirect
from .models import Livro
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('wordnet')
nltk.download('omw-1.4')

def graf(request):
    livros = Livro.objects.all()
    df = pd.DataFrame.from_records(livros.values())

    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')

    df_grouped = df.groupby('review_score')['price'].mean().reset_index()

    fig = px.bar(
        df_grouped,
        x = 'review_score',
        y = 'price',
        title = 'Preço médio por avaliação',
        labels = {'review_score': "Avaliação", 'price': 'Preço Médio (R$)'},
        template = 'plotly_white'
    )

    plot_div = fig.to_html(full_html=False)
    context = {
        'plot_div': plot_div
    }
    return render(request, 'graf.html', context)

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

# def rotular(request):
#     livros = Livro.objects.all()
#     df = pd.DataFrame.from_records(livros.values())   
#     df = df.dropna()

#     lemmatizer = WordNetLemmatizer()

#     def lemmatizar(texto):
#         return ''.join([lemmatizer.lemmatize(palavra) for palavra in texto.split()])

#     reviews_lematizados = [lemmatizar(review) for review in df['review_text']]

#     vet = TfidfVectorizer(
#         stop_words='english', # remove palavras frequentes
#         lowercase=True,       # transforma todas as letras em minusculo
#         max_features=500,     # limitar o lexico em 500 features
#         dtype=np.float32
#     )

#     # aplicar o TF-IDF na coluna review/text
#     tfidf = vet.fit_transform(reviews_lematizados)
#     df_tfidf = pd.DataFrame(tfidf.toarray(), columns=vet.get_feature_names_out())

#     # for col in df_tfidf.columns:
#     #     print(col)

#     # definição dos intervalos e os rotulos
#     bins = [0.99, 2.0, 3.0, 5.0]
#     labels = ['negativo', 'neutro', 'positivo']

#     df['rotulo'] = pd.cut(df['review_score'], bins=bins, labels=labels)

#     df_tfidf_reset = df_tfidf.reset_index(drop=True)
#     df_amostra_reset = df.reset_index(drop=True)

#     df_tfidf_concat = pd.concat([df_tfidf_reset, df_amostra_reset['rotulo']], axis=1)
#     print(df_tfidf_concat)
#     # context = {
#     #     'rotulos': df_tfidf_concat
#     # }
#     # return render(request, 'teste.html', context)

