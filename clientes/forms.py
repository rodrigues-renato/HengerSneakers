from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import authenticate, forms as _forms, password_validation
from .models import CustomUser, EnderecoUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm


class UserChangeForm(_forms.UserChangeForm):
    class Meta(_forms.UserChangeForm.Meta):
        models = CustomUser


class UserCreationForm(_forms.UserCreationForm):
    class Meta(_forms.UserCreationForm.Meta):
        models = CustomUser


class AuthenticationForm(_forms.AuthenticationForm):
    username = forms.EmailField(
        label="E-Mail",
        widget=forms.EmailInput(
            attrs={
                'autocomplete': 'email',
                'class': 'form-control',
                'placeholder': 'Digite seu E-mail',
            }
        ),
        required=True,
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control',
                'placeholder': 'Digite sua senha',
            }
        ),
        required=True,
    )

    class Meta:
        fields = ("username", "password")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if self.user_cache is None:
                if CustomUser.objects.filter(username=username).exists():
                    self.add_error(
                        'password',
                        ValidationError('Senha inválida.', code='invalid'),
                    )
                else:
                    self.add_error(
                        'username',
                        ValidationError('Usuário não cadastrado.', code='invalid'),
                    )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RegisterForm(UserCreationForm):
    cpf = forms.CharField(
        label="CPF",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}
        ),
        required=True,
    )
    telefone = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}
        ),
        required=True,
    )

    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}
        ),
        required=True,
    )

    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'}
        ),
        required=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'cpf',
            'telefone',
            'password1',
            'password2',
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-Mail',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Digite seu sobrenome'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Digite seu e-mail'}
            ),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            self.add_error(
                'first_name', ValidationError('Nome é obrigatório.', code='invalid')
            )
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            self.add_error(
                'last_name', ValidationError('Sobrenome é obrigatório.', code='invalid')
            )
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            self.add_error(
                'email', ValidationError('E-mail é obrigatório.', code='required')
            )
        if CustomUser.objects.filter(email=email).exists():
            self.add_error(
                'email', ValidationError('E-mail já cadastrado.', code='invalid')
            )

        return email

    def clean_cpf(self):
        from utils.functions import valida_cpf

        cpf = self.cleaned_data.get('cpf')
        validador = valida_cpf(cpf)
        if CustomUser.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', ValidationError('CPF já cadastrado.', code='invalid'))
        if not validador:
            self.add_error('cpf', ValidationError('CPF inválido.', code='invalid'))

        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    rua = forms.CharField(
        label="Rua",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua rua',
                'id': 'rua_input',
                'name': 'rua',
            }
        ),
        required=True,
    )

    bairro = forms.CharField(
        label="Bairro",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua bairro',
                'id': 'bairro_input',
                'name': 'bairro',
            }
        ),
        required=True,
    )

    numero = forms.CharField(
        label="Número",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu numero',
                'id': 'numero_input',
                'name': 'numero',
            }
        ),
        required=True,
    )
    class Meta:
        model = EnderecoUser
        fields = ('rua', 'bairro', 'numero')


class UserUpdateForm(forms.ModelForm):
    telefone = forms.CharField(
        label="Telefone",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite seu telefone'}
        ),
        required=True,
    )

    old_password = forms.CharField(
        label="Senha antiga",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}
        ),
        required=False,
    )

    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Digite sua nova senha'}
        ),
        required=False,
    )

    new_password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirme sua nova senha'}
        ),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ('telefone',)

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('new_password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'new_password2', ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        
        if old_password and not self.instance.check_password(old_password):
            self.add_error('old_password', ValidationError('Senha incorreta'))

        return old_password        

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')

        if new_password1:
            try:
                password_validation.validate_password(new_password1)
            except ValidationError as errors:
                self.add_error('new_password1', ValidationError(errors))

        return new_password1

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        current_telefone = self.instance.telefone
        if telefone != current_telefone:
            if CustomUser.objects.filter(telefone=telefone).exists():
                self.add_error(
                    'telefone', ValidationError('Telefone já cadastrado.', code='required')
                )

        return telefone


class EnderecoUpdateForm(forms.ModelForm):
    rua = forms.CharField(
        label="Rua",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua rua',
                'id': 'rua_input',
                'name': 'rua',
            }
        ),
        required=True,
    )

    bairro = forms.CharField(
        label="Bairro",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua bairro',
                'id': 'bairro_input',
                'name': 'bairro',
            }
        ),
        required=True,
    )

    numero = forms.CharField(
        label="Número",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu numero',
                'id': 'numero_input',
                'name': 'numero',
            }
        ),
        required=True,
    )

    class Meta:
        model = EnderecoUser
        fields = ['rua', 'bairro', 'numero']
