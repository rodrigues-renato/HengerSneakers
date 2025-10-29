from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)


class EnderecoUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rua = models.CharField(max_length=80)
    bairro = models.CharField(max_length=80)
    numero = models.CharField(max_length=10)
