import os
import sys
from pathlib import Path
from random import choice, randint
import django
from django.conf import settings
from functions import calcula_valor_total_carrinho

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'henger.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker

    from pedidos.models import Carrinho, ItemCarrinho, Pedido, ItemPedido
    from menu.models import Produto
    fake = faker.Faker('pt_BR')

    pedidos:list[Pedido] = []
    item_carrinho = []
    query_produtos = Produto.objects.all()
    query_carrinhos = Carrinho.objects.all()
    pagamento = ['cartao', 'dinheiro', 'pix']

    for _ in range(NUMBER_OF_OBJECTS):
        carrinho = choice(query_carrinhos)
        for qtd_produtos_no_carrinho in range(randint(1, 10)):
            produto = choice(query_produtos)
            qtd_produtos = randint(1, 10)
            
            item_carrinho.append(ItemCarrinho(
                carrinho=carrinho,
                produto=produto,
                quantidade=qtd_produtos
            ))
        ItemCarrinho.objects.bulk_create(item_carrinho)
        
        pagamento = choice(pagamento)
        cliente = carrinho.cliente
        ic = ItemCarrinho.objects.filter(carrinho=carrinho)
        p = Pedido.objects.create(
            cliente=cliente,
            carrinho=carrinho,
            total=calcula_valor_total_carrinho(ic),
            endereco_envio=fake.address(),
            metodo_pagamento=pagamento
        )
        
        p.finalizar_pedido()
