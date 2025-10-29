from django.urls import path
from . import views
app_name = 'menu'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.index, name='index_alt'),
    path('buscar/', views.buscar, name='buscar'),
    path('produto/<str:id>/', views.produto_detalhado, name='produto_detalhado'),
    path('adicionar_ao_carrinho/<str:id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<str:id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('excluir_do_carrinho/<str:id>/', views.excluir_do_carrinho, name='excluir_do_carrinho'),
]