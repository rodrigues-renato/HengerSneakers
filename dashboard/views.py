from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from pedidos.models import ItemPedido
from menu.models import Produto
from datetime import datetime
from django.db.models import Count,Sum
from collections import Counter


def graph(request):
    if not request.user.is_superuser:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'graph.html')



# def retorna_total_vendido(request):
#     total = ItemPedido.objects.all().aggregate(Sum('total'))['total__sum']
#     if request.method == "GET":
#         return JsonResponse({'total': total})



def relatorio_faturamento(request):
    x = ItemPedido.objects.all()
    
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    cont = 0
    mes = 0
    ano = datetime.now().year
    print(x)
    for m in range(0,12): 
        
        # if mes == 0:
        #     mes = 12
        #     ano -= 1
        
        y = sum([i.produto.preco * i.quantidade for i in x if i.data.month == m+1 and i.data.year == ano])
        
        labels.append(meses[m])
        data.append(y)
        cont += 1
        print(data, labels)
    data_json = {'data': data[::], 'labels': labels[::]}
     
    return JsonResponse(data_json)


def relatorio_vendas(request):
    x = ItemPedido.objects.all()
    print(x[0], 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels = []
    cont = 0
    mes = 0
    ano = datetime.now().year
    for m in range(0,12): 
        
        # if mes == 0:
        #     mes = 12
        #     ano -= 1
        
        y = sum([i.quantidade for i in x if i.data.month == m+1 and i.data.year == ano])
        
        labels.append(meses[m])
        data.append(y)
        cont += 1
        print(data, labels)
    data_json = {'data': data[::], 'labels': labels[::]}
     
    return JsonResponse(data_json)

def relatorio_produtos(request):
    produtos = (ItemPedido.objects
          .select_related('menu__produto')  # Fazendo a junção com a tabela Produto
          .values('produto__categoria')  # Incluindo a categoria do produto
          .annotate(total=Count('id')))  
    print(produtos)
    label = []
    data = []
    for produto_unico in produtos:
        # quantidade_vendas = ItemPedido.objects.filter(produto=produto_unico).aggregate(Count('id'))
        # print(quantidade_vendas)
        if not produto_unico['total']:
            produto_unico['total'] = 0
        label.append(produto_unico['produto__categoria'])
        data.append(produto_unico['total'])

    x = list(zip(label, data))

    x.sort(key=lambda x: x[1], reverse=True)
    x = list(zip(*x))
    print(x)
    return JsonResponse({'labels': x[0][:], 'data': x[1][:]})


def relatorio_clientes(request):
    x = ItemPedido.objects.all().distinct('cliente_id')
    
    pedidos = ItemPedido.objects.all().order_by('cliente_id', 'data')


    pedidos_filtrados = {}
    ano_atual = datetime.now().year

    for pedido in pedidos:
        mes_ano = (pedido.cliente_id, pedido.data.year, pedido.data.month)  # Chave única para cliente/mês
        if mes_ano not in pedidos_filtrados:
            pedidos_filtrados[mes_ano] = pedido  # Mantemos apenas o primeiro encontrado

    # Convertendo para lista
    pedidos_filtrados = list(pedidos_filtrados.values())

    # Agora podemos calcular o total de quantidades por mês
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    data = []
    labels=[]
    for m in range(1, 13):  # De 1 a 12 para os meses
        total_quantidade = sum(p.quantidade for p in pedidos_filtrados if p.data.month == m and p.data.year == ano_atual)
        data.append(total_quantidade)
        labels.append(meses[m-1])
        
        print(data, labels)
    data_json2 = {'data': data[::], 'labels': labels[::]}
     
    return JsonResponse(data_json2)





def relatorio_pizza(request):
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    print("to aquiiiiiiiiiiiiiiiiiiiii")
    # Filtra todos os itens do mês atual (sem usar Strftime)
    itens = ItemPedido.objects.select_related('produto').filter(produto__categoria='Pizza')

    # Filtra manualmente usando Python
    itens_filtrados = [item for item in itens if item.data.month == mes_atual and item.data.year == ano_atual]

    # Conta os produtos
    contador = Counter()
    for item in itens_filtrados:
        contador[item.produto.nome] += 1
    print("to aquiiiiiiiiiiiiiiiiiiiii")
    # Pega os 5 mais vendidos
    mais_vendidos = contador.most_common(5)
    labels = [nome for nome, _ in mais_vendidos]
    data = [quantidade for _, quantidade in mais_vendidos]
    print(labels,data)
    return JsonResponse({'labels': labels, 'data': data})
    #return JsonResponse({'labels': x[0][:], 'data': x[1][:]})