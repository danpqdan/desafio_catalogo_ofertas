from django.urls import path
from .views import filtrar_produto, listar_produtos, atualizar_produtos

urlpatterns = [
    path('', listar_produtos, name='listar_produtos'),
    path('filtrar/', filtrar_produto, name='filtrar_produto'),
    path('atualizar/', atualizar_produtos, name='atualizar_produtos'),
]
