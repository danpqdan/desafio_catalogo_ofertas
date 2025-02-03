from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.URLField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_sem_desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentual_desconto = models.FloatField(null=True, blank=True)
    parcelamento = models.CharField(max_length=100, null=True, blank=True)
    link = models.URLField()
    tipo_entrega = models.CharField(max_length=50, null=True, blank=True)
    frete_gratis = models.BooleanField(default=False)

    def __str__(self):
        return self.nome