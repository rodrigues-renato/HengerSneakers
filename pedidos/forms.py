from django import forms
from django.contrib.auth import forms as form_user
from .models import CustomUser
from django.core.exceptions import ValidationError

class PedidoForm(forms.Form):
    endereco_envio = forms.TextInput()
    