from django.contrib import admin
from .models import *


class ItemCarrinhoInline(admin.TabularInline):
    """Inline para exibir itens do carrinho dentro do Carrinho"""
    model = ItemCarrinho
    extra = 0
    fields = ('detalhe_produto', 'quantidade', 'get_total')
    readonly_fields = ('get_total',)
    
    def get_total(self, obj):
        if obj.id:
            return f'R$ {obj.get_total():.2f}'
        return '-'
    get_total.short_description = 'Total'


class ItemPedidoInline(admin.TabularInline):
    """Inline para exibir itens do pedido dentro do Pedido"""
    model = ItemPedido
    extra = 0
    fields = ('detalhe_produto', 'quantidade', 'preco_unitario', 'get_total')
    readonly_fields = ('get_total', 'preco_unitario', 'detalhe_produto', 'quantidade')
    
    def get_total(self, obj):
        if obj.id:
            return f'R$ {obj.get_total():.2f}'
        return '-'
    get_total.short_description = 'Total Item'


@admin.register(ItemCarrinho)
class ItemCarrinhoAdmin(admin.ModelAdmin):
    list_display = ('carrinho', 'get_produto_nome', 'get_variante_info', 'quantidade', 'get_preco', 'get_total_display')
    list_filter = ('carrinho__cliente',)
    search_fields = ('detalhe_produto__produto__nome', 'carrinho__cliente__username')
    readonly_fields = ('get_total_display',)
    
    def get_produto_nome(self, obj):
        return obj.detalhe_produto.produto.nome
    get_produto_nome.short_description = 'Produto'
    
    def get_variante_info(self, obj):
        return f'{obj.detalhe_produto.cor.nome} - Tam {obj.detalhe_produto.tamanho} - {obj.detalhe_produto.genero}'
    get_variante_info.short_description = 'Variante'
    
    def get_preco(self, obj):
        return f'R$ {obj.detalhe_produto.preco:.2f}'
    get_preco.short_description = 'Preço Unit.'
    
    def get_total_display(self, obj):
        return f'R$ {obj.get_total():.2f}'
    get_total_display.short_description = 'Total'


@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'get_total_itens', 'get_valor_total')
    list_filter = ('cliente',)
    search_fields = ('cliente__username', 'cliente__email')
    inlines = [ItemCarrinhoInline]
    
    def get_total_itens(self, obj):
        return obj.itens.count()
    get_total_itens.short_description = 'Qtd Itens'
    
    def get_valor_total(self, obj):
        from utils.functions import calcula_valor_total_carrinho
        total = calcula_valor_total_carrinho(obj.id)
        return f'R$ {total:.2f}'
    get_valor_total.short_description = 'Valor Total'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'get_total_display', 'metodo_pagamento', 'get_qtd_itens', 'criado_em')
    list_filter = ('metodo_pagamento', 'criado_em')
    search_fields = ('cliente__username', 'cliente__email')
    readonly_fields = ('criado_em', 'get_total_display')
    inlines = [ItemPedidoInline]
    date_hierarchy = 'criado_em'
    
    def get_total_display(self, obj):
        return f'R$ {obj.total:.2f}'
    get_total_display.short_description = 'Total'
    
    def get_qtd_itens(self, obj):
        return obj.itens.count()
    get_qtd_itens.short_description = 'Qtd Itens'


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'cliente', 'get_produto_nome', 'get_variante_info', 'quantidade', 'get_preco_unitario', 'get_total_display', 'data')
    list_filter = ('pedido__criado_em', 'cliente')
    search_fields = ('detalhe_produto__produto__nome', 'cliente__username', 'pedido__id')
    readonly_fields = ('get_total_display', 'data')
    date_hierarchy = 'data'
    
    def get_produto_nome(self, obj):
        return obj.detalhe_produto.produto.nome
    get_produto_nome.short_description = 'Produto'
    
    def get_variante_info(self, obj):
        return f'{obj.detalhe_produto.cor.nome} - Tam {obj.detalhe_produto.tamanho} - {obj.detalhe_produto.genero}'
    get_variante_info.short_description = 'Variante'
    
    def get_preco_unitario(self, obj):
        return f'R$ {obj.preco_unitario:.2f}'
    get_preco_unitario.short_description = 'Preço Unit.'
    
    def get_total_display(self, obj):
        return f'R$ {obj.get_total():.2f}'
    get_total_display.short_description = 'Total'
