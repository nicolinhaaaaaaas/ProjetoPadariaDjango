from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # TELAS #
    path('', views.principalGerente, name='gerenciamento'),
    path('perfilGerente/', views.perfil, name='perfilGerente'),
    path('principalGerente/', views.principalGerente, name='principalGerente'),
    path('listaPedidos/', views.lista_pedidos, name='listaPedidos'),
    path('pedido/<int:id_pedido>', views.pedido, name='pedido'),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('addFuncionario/', views.addFuncionario, name='addFuncionario'),
    path('updateFuncionario/<int:id_funcionario>', views.attFuncionario, name='updateFuncionario'),
    path('addProduto/', views.addProduto, name='addProduto'),
    path('updateProduto/<int:id_produto>', views.attProduto, name='updateProduto'),
    path('clientes/' , views.clientes, name='clientes'),
    path('pesquisaProduto/', views.pesquisaProduto, name='pesquisaProduto'),
    path('buscar_sugestao/', views.buscar_sugestoes, name='buscar_sugestoes'),
    path('notaPedido/<int:id_pedido>', views.notaPedido, name='notaPedido'),

    # FUNÇÕES DE DADOS #
    path('dados_funcionario/', views.dadosFuncionario, name='dados_funcionario'),
    path('dados_produto/', views.dadosProduto, name='dados_produto'),
    path('dados_pedido/', views.dadosPedido, name='dados_pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)