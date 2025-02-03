from django.shortcuts import render

from django.shortcuts import render
from .models import Produto
from .utils import buscar_mercado_livre

def atualizar_produtos(request):
    buscar_mercado_livre()
    return listar_produtos(request)

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'busca_produtos.html', {'produtos': produtos})

