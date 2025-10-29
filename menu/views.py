from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from menu.models import Produto, DetalheProduto
from pedidos.models import ItemCarrinho, Carrinho, Pedido
from clientes.models import CustomUser
from utils.functions import calcula_valor_total_carrinho
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse


@login_required(login_url='clientes:login_cliente')
def index(request):
    """
    Primeira tela do site.
    Exibe os produtos com informações agregadas dos detalhes
    """
    from django.db.models import Min, Sum, Count
    
    # Get products with aggregated data from DetalheProduto
    produtos = Produto.objects.annotate(
        preco_minimo=Min('detalhes__preco'),
        estoque_total=Sum('detalhes__estoque'),
        qtd_variantes=Count('detalhes')
    ).filter(qtd_variantes__gt=0).order_by('nome')
    
    paginator = Paginator(produtos, 12)  # 12 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    usuario = get_object_or_404(CustomUser, username=request.user)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)

    # Incorporacao da view carrinho_detalhado
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado).first()
    if subtotal:
        subtotal = subtotal.get_total()
    else:
        subtotal = 0
    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()

    context = {
        'page_obj': page_obj,
        'carrinho': carrinho_vinculado,
        'qtd_item_carrinho': qtd_itens_carrinho,
        'item_carrinho': item_carrinho,
        'produtos': produtos,
        'subtotal': subtotal,
    }

    return render(request, 'menu/index.html', context)


@login_required(login_url='clientes:login_cliente')
def buscar(request):
    from django.db.models import Min, Sum, Count
    
    usuario = get_object_or_404(CustomUser, username=request.user)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()

    query = request.GET.get("q", '').strip()
    if query == "":
        return redirect('menu:index')

    produtos = Produto.objects.filter(
        Q(nome__icontains=str(query))
        | Q(descricao__icontains=str(query))
        | Q(marca__nome__icontains=str(query))
    ).annotate(
        preco_minimo=Min('detalhes__preco'),
        estoque_total=Sum('detalhes__estoque'),
        qtd_variantes=Count('detalhes')
    ).filter(qtd_variantes__gt=0).order_by('nome')
    
    paginator = Paginator(produtos, 12)  # 12 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)
    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()

    context = {
        'page_obj': page_obj,
        'carrinho': carrinho_vinculado,
        'qtd_item_carrinho': qtd_itens_carrinho,
        'item_carrinho': item_carrinho,
        'produtos': produtos,
        'subtotal': subtotal,
        'query': query,
    }

    return render(request, 'menu/index.html', context)


@login_required(login_url='clientes:login_cliente')
def adicionar_ao_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(produto=produto, carrinho=carrinho_vinculado)
    if consulta.exists():
        item = consulta.first()
        item.quantidade += 1
        item.save()

    else:
        item = ItemCarrinho.objects.create(
            produto=produto,
            carrinho=carrinho_vinculado,
            quantidade=1,
        )

    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)
    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()

    # messages.info(request, f'{produto.nome} adicionado ao carrinho')
    # return redirect(request.META.get('HTTP_REFERER', 'menu:index'))
    print(
        {
            "status": "success",
            "message": f"{produto.nome} adicionado ao carrinho",
            "quantidade": item.quantidade,
            "total": item.get_total(),
            "produto_id": item.produto.id,
            "total_price": subtotal,
        }
    )

    return JsonResponse(
        {
            "status": "success",
            "message": f"{produto.nome} adicionado ao carrinho",
            "quantidade": item.quantidade,
            "total": item.get_total(),
            "produto_id": item.produto.id,
            'qtd_item_carrinho': qtd_itens_carrinho,
            "total_price": subtotal,
            "produto_nome": produto.nome,
        }
    )


@login_required(login_url='clientes:login_cliente')
def remover_do_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(
        produto=produto, carrinho=carrinho_vinculado
    ).first()
    if consulta:
        if consulta.quantidade > 1:
            consulta.quantidade -= 1
            consulta.save()
            quantidade_atual = consulta.quantidade
        elif consulta.quantidade == 1:
            consulta.delete()
            quantidade_atual = 0
    else:
        return JsonResponse(
            {"status": "error", "message": "Produto não encontrado no carrinho"},
            status=400,
        )

    # messages.warning(request, f'{produto.nome} removido do carrinho')
    # return redirect(request.META.get('HTTP_REFERER', 'menu:index'))
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)
    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()

    print(
        {
            "status": "success",
            "message": f"{produto.nome} removido do carrinho",
            "quantidade": quantidade_atual,
            "total": consulta.get_total() if quantidade_atual > 0 else 0,
            "produto_id": produto.id,
            "total_price": subtotal,
        }
    )
    return JsonResponse(
        {
            "status": "success",
            "message": f"{produto.nome} removido do carrinho",
            "quantidade": quantidade_atual,
            "total": consulta.get_total() if quantidade_atual > 0 else 0,
            'qtd_item_carrinho': qtd_itens_carrinho,
            "produto_id": produto.id,
            "total_price": subtotal,
        }
    )


@login_required(login_url='clientes:login_cliente')
def excluir_do_carrinho(request, id):
    usuario = get_object_or_404(CustomUser, username=request.user)

    produto = get_object_or_404(Produto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    consulta = ItemCarrinho.objects.filter(
        produto=produto, carrinho=carrinho_vinculado
    ).first()
    if consulta.quantidade >= 1:
        consulta.delete()

    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()
    # messages.error(request, f'{produto.nome} excluído do carrinho')
    # return redirect(request.META.get('HTTP_REFERER', 'menu:index'))
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)

    return JsonResponse(
        {
            "status": "success",
            "message": f"{produto.nome} excluído do carrinho",
            "quantidade": 0,
            'qtd_item_carrinho': qtd_itens_carrinho,
            "produto_id": produto.id,
            "total_price": subtotal,
        }
    )


@login_required(login_url='clientes:login_cliente')
def produto_detalhado(request, id):
    """
    Exibe detalhes completos de um produto com todas as variações
    de tamanho, cor e gênero disponíveis
    """
    produto = get_object_or_404(Produto, id=id)
    usuario = get_object_or_404(CustomUser, username=request.user)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    
    # Buscar todos os detalhes do produto (variações)
    detalhes = produto.detalhes.all().select_related('cor')
    
    # Agrupar tamanhos, cores e gêneros disponíveis
    tamanhos_disponiveis = detalhes.values_list('tamanho', flat=True).distinct().order_by('tamanho')
    cores_disponiveis = detalhes.values_list('cor__nome', 'cor__id').distinct()
    generos_disponiveis = detalhes.values_list('genero', flat=True).distinct()
    
    # Calcular estoque total e preço (usar o menor preço)
    estoque_total = sum(d.estoque for d in detalhes)
    preco_minimo = min(d.preco for d in detalhes) if detalhes else 0
    preco_maximo = max(d.preco for d in detalhes) if detalhes else 0
    
    # Informações do carrinho
    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)

    context = {
        'produto': produto,
        'detalhes': detalhes,
        'tamanhos_disponiveis': tamanhos_disponiveis,
        'cores_disponiveis': cores_disponiveis,
        'generos_disponiveis': generos_disponiveis,
        'estoque_total': estoque_total,
        'preco_minimo': preco_minimo,
        'preco_maximo': preco_maximo,
        'qtd_item_carrinho': qtd_itens_carrinho,
        'item_carrinho': item_carrinho,
        'subtotal': subtotal,
        'carrinho': carrinho_vinculado,
    }

    return render(request, 'menu/produto_detalhado.html', context)