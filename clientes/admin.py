from django.contrib import admin
from clientes.models import CustomUser, EnderecoUser
from django.contrib.auth import admin as admin_auth


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = 'id', 'username'


@admin.register(EnderecoUser)
class EnderecoUserAdmin(admin.ModelAdmin):
    list_display = 'user', 'rua', 'bairro', 'numero'
