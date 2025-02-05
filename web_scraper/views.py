from django.shortcuts import render,redirect

from django.shortcuts import render
from .models import Produto
from .utils import buscar_mercado_livre

def atualizar_produtos(request):
    if request.method == "POST":
        termo_busca = request.POST.get('termo_busca')
        if termo_busca:
            buscar_mercado_livre(termo_busca=termo_busca)
            return redirect('listar_produtos')
    return render(request, 'busca_produtos.html')

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'busca_produtos.html', {'produtos': produtos})

def filtrar_produto(request):
    query = request.GET.get('q', '')
    frete_gratis = request.GET.get('frete_gratis')
    tipo_entrega = request.GET.get('tipo_entrega', None)
    ordenar_por = request.GET.get('ordenar_por', None)

    produtos = Produto.objects.all()
    if query:
        try:
            produtos = produtos.filter(nome__icontains=query)
        except:
            produtos = []
    if frete_gratis:
        try:
            produtos = produtos.filter(frete_gratis=True)
        except:
            produtos = []
    
    if tipo_entrega == 'Full':
        produtos = produtos.filter(tipo_entrega='Full')

    if ordenar_por == 'preco_maior':
        produtos = produtos.order_by('-preco')
    elif ordenar_por == 'preco_menor':
        produtos = produtos.order_by('preco') 
    elif ordenar_por == 'desconto_maior':
        produtos = produtos.order_by('-percentual_desconto')

    return render(request, 'busca_produtos.html', {'produtos': produtos})




