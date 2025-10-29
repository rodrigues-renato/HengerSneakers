from django.contrib import admin
from menu.models import Produto, DetalheProduto, Marca, Cor


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)


@admin.register(Cor)
class CorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)


class DetalheProdutoInline(admin.TabularInline):
    """Inline para gerenciar variantes do produto (tamanho, cor, gênero)"""
    model = DetalheProduto
    extra = 1
    fields = ('tamanho', 'cor', 'genero', 'preco', 'estoque', 'sku')
    autocomplete_fields = ['cor']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'marca', 'get_total_estoque', 'get_qtd_variantes')
    list_filter = ('marca',)
    search_fields = ('nome', 'marca__nome', 'descricao')
    ordering = ('-id',)
    autocomplete_fields = ['marca']
    inlines = [DetalheProdutoInline]
    
    def get_total_estoque(self, obj):
        """Mostra o estoque total de todas as variantes"""
        total = sum(d.estoque for d in obj.detalhes.all())
        return total
    get_total_estoque.short_description = 'Estoque Total'
    
    def get_qtd_variantes(self, obj):
        """Mostra quantas variantes o produto possui"""
        return obj.detalhes.count()
    get_qtd_variantes.short_description = 'Variantes'


@admin.register(DetalheProduto)
class DetalheProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'produto', 'tamanho', 'cor', 'genero', 'preco', 'estoque', 'sku')
    list_filter = ('produto__marca', 'tamanho', 'cor', 'genero')
    search_fields = ('produto__nome', 'produto__marca__nome', 'cor__nome', 'sku')
    ordering = ('produto', 'tamanho', 'cor')
    autocomplete_fields = ['produto', 'cor']
    list_editable = ('preco', 'estoque')
    
    fieldsets = (
        ('Produto', {
            'fields': ('produto',)
        }),
        ('Variante', {
            'fields': ('tamanho', 'cor', 'genero')
        }),
        ('Preço e Estoque', {
            'fields': ('preco', 'estoque', 'sku')
        }),
    )
