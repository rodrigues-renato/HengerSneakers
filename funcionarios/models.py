from clientes.models import CustomUser
from django.db import models

class Funcionario(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cargo = models.CharField(
        max_length=50,
        choices=[("Atendente", "Atendente"), ("Motoboy", "Motoboy")]
    )
