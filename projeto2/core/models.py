from django.db import models

class Livro(models.Model):
    titulo = models.CharField("Título", max_length=100)
    genero = models.CharField("Gênero", max_length=60, null=True)
    data_publicacao = models.DateField("Data de publicação",null=True)
    numero_paginas = models.PositiveIntegerField("Páginas")
    estoque = models.PositiveIntegerField("Quantidade", null=True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8)

    def __str__(self):
        return self.titulo

class Autor(models.Model):
    nome = models.CharField("Nome", max_length=100)
    nacionalidade = models.CharField("Nacionalidade", max_length=100)
    pseudonimo = models.CharField("Pseudônimo", max_length=100)
    data_nasc = models.DateField("Data de nascimento", null=True, blank=True)
    data_falec = models.DateField("Data falecimento", null=True, blank=True)

    def __str__(self):
        return self.nome
