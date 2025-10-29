from django.contrib import admin
from funcionarios.models import Funcionario

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = 'usuario', 'cargo'
    ordering = '-id',
