from django.shortcuts import render,redirect

from django.shortcuts import render
from .models import Produto
from .utils import buscar_mercado_livre

def atualizar_produtos(request):
    if request.method == "POST":
        termo_busca = request.POST.get('termo_busca')  # Obtém o valor do input de busca
        if termo_busca:
            buscar_mercado_livre(termo_busca=termo_busca)  # Chama a função de raspagem
            return redirect('listar_produtos')  # Redireciona para a página de listagem dos produtos
    return render(request, 'atualizar_produtos.html')  # Caso não seja POST, retorna o formulário

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'busca_produtos.html', {'produtos': produtos})

def filtrar_produto(request):
    query = request.GET.get('q', '')  # Obtém o valor da busca
    frete_gratis = request.GET.get('frete_gratis')  # Filtra produtos com frete grátis
    tipo_entrega = request.GET.get('tipo_entrega', None)  # Filtra produtos entregues pelo Full
    ordenar_por = request.GET.get('ordenar_por', None)  # Ordenação por preço ou desconto

    produtos = Produto.objects.all()

    # Filtrando produtos por nome
    if query:
        try:
            produtos = produtos.filter(nome__icontains=query)
        except:
            produtos = []

    # Filtrando produtos com frete grátis
    if frete_gratis:
        try:
            produtos = produtos.filter(frete_gratis=True)
        except:
            produtos = []
    
    # Filtrando produtos entregues pelo Full
    if tipo_entrega == 'Full':
        produtos = produtos.filter(tipo_entrega='Full')

    # Ordenação
    if ordenar_por == 'preco_maior':
        produtos = produtos.order_by('-preco')  # Ordena pelo maior preço
    elif ordenar_por == 'preco_menor':
        produtos = produtos.order_by('preco')  # Ordena pelo menor preço
    elif ordenar_por == 'desconto_maior':
        produtos = produtos.order_by('-percentual_desconto')  # Ordena pelo maior desconto

    return render(request, 'busca_produtos.html', {'produtos': produtos})




