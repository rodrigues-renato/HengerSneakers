from django.db import models
from clientes.models import CustomUser
from menu.models import Produto, DetalheProduto
from django.db import transaction


class Carrinho(models.Model):
    cliente = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrinho de {self.cliente.username}"


class ItemCarrinho(models.Model):
    """
    Item no carrinho de compras.
    Referencia DetalheProduto (variante específica com tamanho, cor, gênero).
    """
    detalhe_produto = models.ForeignKey(DetalheProduto, on_delete=models.CASCADE, related_name='itens_carrinho')
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, related_name='itens')
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade}x {self.detalhe_produto}"

    def get_total(self):
        """Calcula o total do item (quantidade × preço da variante)"""
        return self.detalhe_produto.preco * self.quantidade
    
    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens do Carrinho'


class Pedido(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pedidos')
    carrinho = models.ForeignKey(
        Carrinho, on_delete=models.SET_NULL, null=True, blank=True
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    endereco_envio = models.TextField()
    metodo_pagamento = models.CharField(
        max_length=20,
        choices=[
            ('cartao_credito', 'Cartão de Crédito'),
            ('cartao_debito', 'Cartão de Débito'),
            ('pix', 'Pix'),
            ('boleto', 'Boleto')
        ],
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def finalizar_pedido(self):
        """Finaliza o pedido criando ItemPedido para cada item do carrinho"""
        if self.carrinho:
            with transaction.atomic():
                itens_carrinho = ItemCarrinho.objects.filter(carrinho=self.carrinho)

                for item in itens_carrinho:
                    ItemPedido.objects.create(
                        pedido=self,
                        detalhe_produto=item.detalhe_produto,
                        quantidade=item.quantidade,
                        preco_unitario=item.detalhe_produto.preco,  # Salva o preço no momento da compra
                        cliente=self.cliente,
                    )

                itens_carrinho.delete()

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username}"
    
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class ItemPedido(models.Model):
    """
    Item de um pedido finalizado.
    Armazena snapshot do produto comprado (preço no momento da compra).
    """
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='itens_pedidos')
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    detalhe_produto = models.ForeignKey(DetalheProduto, on_delete=models.PROTECT, related_name='itens_pedidos')
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, help_text="Preço no momento da compra")
    data = models.DateTimeField(auto_now_add=True)
 
    def get_total(self):
        """Calcula o total do item usando o preço salvo"""
        return self.preco_unitario * self.quantidade
    
    def __str__(self):
        return f"{self.quantidade}x {self.detalhe_produto} - Pedido #{self.pedido.id}"
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens dos Pedidos'
        ordering = ['-data']
