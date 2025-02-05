from django.db import models

class Produto(models.Model):
    nome = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_sem_desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentual_desconto = models.FloatField(null=True, blank=True)
    parcelamento = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField()
    tipo_entrega = models.CharField(max_length=50, null=True, blank=True)
    frete_gratis = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    
class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, related_name="imagens", on_delete=models.CASCADE)
    url_imagem = models.URLField()

    def __str__(self):
        return f"Imagem de {self.produto.nome}"
