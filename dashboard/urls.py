from django.urls import path
from . import views

app_name = 'dashboard'


urlpatterns = [
    path('', views.graph, name="graph"),
    # path('retorna_total_vendido', views.retorna_total_vendido, name="retorna_total_vendido"),
    path('relatorio_faturamento', views.relatorio_faturamento, name="relatorio_faturamento"),
    path('relatorio_produtos', views.relatorio_produtos, name="relatorio_produtos"),
    path('relatorio_vendas', views.relatorio_vendas, name="relatorio_vendas"),
    path('relatorio_clientes', views.relatorio_clientes, name="relatorio_clientes"),
    path('relatorio_pizza', views.relatorio_pizza, name="relatorio_pizza"),
    
    
]