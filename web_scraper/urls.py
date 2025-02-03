from django.urls import path
from .views import listar_produtos, atualizar_produtos

urlpatterns = [
    path('', listar_produtos, name='listar_produtos'),
    path('atualizar/', atualizar_produtos, name='atualizar_produtos'),
]
