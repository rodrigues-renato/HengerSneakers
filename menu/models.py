from django.db import models

GENDER_CHOICES = [
    ("M", "Masculino"),
    ("F", "Feminino"),
    ("U", "Unissex"),
    ("I", "Infantil"),
]

SIZE_CHOICES = [
    ("36", "36"),
    ("37", "37"),
    ("38", "38"),
    ("39", "39"),
    ("40", "40"),
    ("41", "41"),
    ("42", "42"),
    ("43", "43"),
    ("44", "44"),
]


class Cor(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name="produtos")
    imagem = models.ImageField(upload_to="sneakers/", blank=True, null=True)

    def __str__(self):
        return f"{self.marca} {self.nome}"


class DetalheProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="detalhes")
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE, related_name="detalhes")
    tamanho = models.CharField(max_length=10, choices=SIZE_CHOICES) 
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES)
    estoque = models.PositiveIntegerField(default=0)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ("produto", "tamanho", "cor", "genero")
        ordering = ("produto", "tamanho", "cor")

    def __str__(self):
        return f"{self.produto.nome} - Tam {self.tamanho} - {self.cor} ({self.get_genero_display()})"
