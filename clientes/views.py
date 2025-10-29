from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AddressForm
from pedidos.models import Carrinho
from clientes.models import CustomUser, EnderecoUser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .forms import (
    UserUpdateForm,
    EnderecoUpdateForm,
    AuthenticationForm,
)
from django.contrib.auth import update_session_auth_hash
from .models import EnderecoUser


def registrar_cliente(request):
    if request.user.is_authenticated:
        return redirect('menu:index')

    user_form = RegisterForm()

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # messages.success(request, 'Usuário criado com sucesso')

            # Quando uma conta é registrada, um carrinho é vinculado a ela
            custom_user = get_object_or_404(
                CustomUser, email=user_form.cleaned_data['email']
            )
            criar_carrinho = Carrinho.objects.create(cliente=custom_user)
            criar_carrinho.save()

            return redirect('clientes:login_cliente')

    context = {'user_form': user_form}
    return render(request, 'clientes/registrar.html', context)


def logar_cliente(request):
    if request.user.is_authenticated:
        return redirect('menu:index')

    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # messages.success(request, 'Logado com sucesso')
            return redirect('menu:index')

    return render(request, 'clientes/logar.html', {'form': form})


@login_required(login_url='clientes:login_cliente')
def deslogar_cliente(request):
    logout(request)
    # messages.success(request, 'Deslogado com sucesso')
    return redirect('clientes:login_cliente')


def salvar_endereco(request):
    rua = request.POST.get('rua')
    bairro = request.POST.get('bairro')
    numero = request.POST.get('numero')
    count = EnderecoUser.objects.filter(
        user=request.user, rua=rua, bairro=bairro, numero=numero
    ).count()
    if count > 0:
        return JsonResponse({"error": "Este endereço já está cadastrado"}, status=400)
    else:
        form = AddressForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.user = request.user
            endereco.save()
            # return redirect(request.META.get('HTTP_REFERER', 'pedidos:finalizar_pedido')) -> Retorno antigo
            return JsonResponse(
                {
                    "id": endereco.id,  # ID do novo endereço
                    "rua": endereco.rua,
                    "bairro": endereco.bairro,
                    "numero": endereco.numero,
                }
            )
        return JsonResponse({"error": "Requisição inválida"}, status=400)

def excluir_endereco(request, id):
    endereco = get_object_or_404(EnderecoUser, id=id)
    if endereco.user == request.user:
        endereco.delete()
        messages.success(request, "Endereço removido com sucesso")
        return redirect('clientes:atualizar_dados')
    


@login_required(login_url='clientes:login_cliente')
def atualizar_dados(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    endereco_update_form = EnderecoUpdateForm(instance=user)
    endereco_create_form = AddressForm(instance=user)
    enderecos = EnderecoUser.objects.filter(user=user)
    manter_logado = AuthenticationForm(request)

    if request.method == "POST":
        print(request.POST)
        endereco_selecionado = request.POST.get('endereco_id')
        endereco = enderecos.filter(id=endereco_selecionado).first()

        user_form = UserUpdateForm(request.POST, instance=user)
        endereco_update_form = EnderecoUpdateForm(request.POST, instance=endereco)

        if user_form.is_valid():
            user_form.save()
            user = manter_logado.get_user()
            login(request, user)
            messages.success(request, "Atualizado com sucesso!")
            return redirect('clientes:atualizar_dados')
       
        if endereco_update_form.is_valid():
            endereco_update_form.save()
            messages.success(request, "Endereço atualizado com sucesso!")
            return redirect('clientes:atualizar_dados')

        if endereco_create_form.is_valid():
            endereco_create_form.save()
            messages.success(request, "Novo endereço cadastrado com sucesso!")
            return redirect('clientes:atualizar_dados')


    return render(
        request,
        'clientes/atualizar_dados.html',
        {
            'user_form': user_form,
            'endereco_form': endereco_update_form,
            'enderecos': enderecos,
            'address_form': endereco_create_form,
        },
    )
