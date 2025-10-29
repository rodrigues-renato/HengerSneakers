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
    """
    Adiciona uma variante específica (DetalheProduto) ao carrinho.
    O 'id' agora se refere ao DetalheProduto (variante com tamanho/cor/gênero específicos)
    """
    usuario = get_object_or_404(CustomUser, username=request.user)
    
    # Buscar o detalhe do produto (variante específica)
    detalhe_produto = get_object_or_404(DetalheProduto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    
    # Verificar se a variante já está no carrinho
    consulta = ItemCarrinho.objects.filter(
        detalhe_produto=detalhe_produto, 
        carrinho=carrinho_vinculado
    )
    
    if consulta.exists():
        item = consulta.first()
        # Verificar se há estoque suficiente
        if item.quantidade < detalhe_produto.estoque:
            item.quantidade += 1
            item.save()
            message = f"{detalhe_produto.produto.nome} (quantidade atualizada)"
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Estoque insuficiente para este item"
                },
                status=400
            )
    else:
        # Verificar se há estoque disponível
        if detalhe_produto.estoque < 1:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Produto sem estoque"
                },
                status=400
            )
        
        item = ItemCarrinho.objects.create(
            detalhe_produto=detalhe_produto,
            carrinho=carrinho_vinculado,
            quantidade=1,
        )
        message = f"{detalhe_produto.produto.nome} adicionado ao carrinho"
    
    # Calcular totais
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)
    qtd_itens_carrinho = item_carrinho.count()

    return JsonResponse(
        {
            "status": "success",
            "message": message,
            "quantidade": item.quantidade,
            "total": float(item.get_total()),
            "variante_id": detalhe_produto.id,
            'qtd_item_carrinho': qtd_itens_carrinho,
            "total_price": float(subtotal),
            "produto_nome": detalhe_produto.produto.nome,
            "variante_info": f"{detalhe_produto.cor.nome} - Tam {detalhe_produto.tamanho}",
        }
    )


@login_required(login_url='clientes:login_cliente')
def remover_do_carrinho(request, id):
    """
    Remove uma unidade de uma variante específica do carrinho.
    O 'id' se refere ao DetalheProduto (variante).
    """
    usuario = get_object_or_404(CustomUser, username=request.user)
    
    detalhe_produto = get_object_or_404(DetalheProduto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    
    consulta = ItemCarrinho.objects.filter(
        detalhe_produto=detalhe_produto, 
        carrinho=carrinho_vinculado
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

    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)
    qtd_itens_carrinho = item_carrinho.count()

    return JsonResponse(
        {
            "status": "success",
            "message": f"{detalhe_produto.produto.nome} removido do carrinho",
            "quantidade": quantidade_atual,
            "total": float(consulta.get_total()) if quantidade_atual > 0 else 0,
            'qtd_item_carrinho': qtd_itens_carrinho,
            "variante_id": detalhe_produto.id,
            "total_price": float(subtotal),
        }
    )


@login_required(login_url='clientes:login_cliente')
def excluir_do_carrinho(request, id):
    """
    Exclui completamente uma variante do carrinho.
    O 'id' se refere ao DetalheProduto (variante).
    """
    usuario = get_object_or_404(CustomUser, username=request.user)
    
    detalhe_produto = get_object_or_404(DetalheProduto, id=id)
    carrinho_vinculado = get_object_or_404(Carrinho, cliente=usuario)
    
    consulta = ItemCarrinho.objects.filter(
        detalhe_produto=detalhe_produto, 
        carrinho=carrinho_vinculado
    ).first()
    
    if consulta:
        consulta.delete()

    qtd_itens_carrinho = ItemCarrinho.objects.filter(
        carrinho=carrinho_vinculado
    ).count()
    
    item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_vinculado)
    subtotal = calcula_valor_total_carrinho(item_carrinho)

    return JsonResponse(
        {
            "status": "success",
            "message": f"{detalhe_produto.produto.nome} excluído do carrinho",
            "quantidade": 0,
            'qtd_item_carrinho': qtd_itens_carrinho,
            "variante_id": detalhe_produto.id,
            "total_price": float(subtotal),
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
    
    # Agrupar tamanhos, cores e gêneros disponíveis (sem duplicatas)
    tamanhos_disponiveis = sorted(set(detalhes.values_list('tamanho', flat=True)))
    cores_disponiveis = list(detalhes.values_list('cor__nome', 'cor__id').distinct())
    generos_disponiveis = sorted(set(detalhes.values_list('genero', flat=True)))
    
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