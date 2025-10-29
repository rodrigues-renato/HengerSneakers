from django.shortcuts import render, get_object_or_404, redirect
from pedidos.models import Pedido, Carrinho, ItemCarrinho, ItemPedido
from clientes.models import CustomUser, EnderecoUser
from utils.functions import calcula_valor_total_carrinho
from django.http import HttpResponse
from clientes.forms import AddressForm
from django.contrib import messages
from django.core.paginator import Paginator


def finalizar_pedido(request):
    address_form = AddressForm()

    if request.method == 'POST':
        usuario = get_object_or_404(CustomUser, username=request.user)
        carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
        item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
        total = calcula_valor_total_carrinho(item_carrinho)
        metodo_pagamento = request.POST.get('metodo_pagamento')
        pedido_esta_correto = True
        
        endereco = request.POST.get('endereco')
        tempo_de_entrega = '5 a 7 dias úteis'
        msg_status_pedido = f'Seu pedido será entregue em {tempo_de_entrega}!'
        
        if not endereco:
            pedido_esta_correto = False
            messages.error(request, 'Por favor, selecione um endereço de entrega')

        if not metodo_pagamento:
            pedido_esta_correto = False
            messages.error(request, 'Por favor, selecione um método de pagamento')

        if pedido_esta_correto:
            pedido = Pedido.objects.create(
                cliente=usuario,
                carrinho=carrinho_vinculado,
                total=total,
                endereco_envio=endereco,
                metodo_pagamento=metodo_pagamento,
            )

            pedido.finalizar_pedido()
            context = {
                'item_carrinho': item_carrinho,
                'pedido': pedido,
                'status_pedido': msg_status_pedido,
                'subtotal': total,
            }
            return render(request, 'pedidos/status_pedido.html', context)

    usuario = get_object_or_404(CustomUser, username=request.user)
    enderecos = EnderecoUser.objects.filter(user=usuario).all()
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    qtd_itens_carrinho = item_carrinho.count()
    if qtd_itens_carrinho == 0:
        return redirect('menu:index')

    total = calcula_valor_total_carrinho(item_carrinho)

    context = {
        'usuario': usuario,
        'carrinho': carrinho_vinculado,
        'enderecos': enderecos,
        'item_carrinho': item_carrinho,
        'qtd_item_carrinho': qtd_itens_carrinho,
        'subtotal': total,
        'address_form': address_form,
    }

    return render(request, 'pedidos/finalizar_pedido.html', context)


def historico_de_pedidos(request):
    usuario = get_object_or_404(CustomUser, username=request.user)
    pedidos = Pedido.objects.filter(cliente=usuario).all().order_by('-criado_em')
    paginator = Paginator(pedidos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    itens_pedidos = ItemPedido.objects.filter(cliente=usuario).all()
    context = {
        'itens_pedidos': itens_pedidos,
        'page_obj': page_obj,
    }
    return render(request, 'pedidos/historico.html', context)
