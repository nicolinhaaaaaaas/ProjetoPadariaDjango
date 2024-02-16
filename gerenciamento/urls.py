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
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('addFuncionario/', views.addFuncionario, name='addFuncionario'),
    path('updateFuncionario/', views.attFuncionario, name='updateFuncionario'),
    path('addProduto/', views.addProduto, name='addProduto'),
    path('updateProduto/<int:id_produto>', views.attProduto, name='updateProduto'),
    path('clientes/' , views.clientes, name='clientes'),
    path('pesquisaProdutoGerente/', views.pesquisarProdutoGerente, name='pesquisaProdutoGerente'),
    path('buscar_sugestao/', views.buscar_sugestoes, name='buscar_sugestoes'),
    path('notaPedido/<int:id_pedido>', views.notaPedido, name='notaPedido'),
    path('produtoGerente/<int:id_produto>/', views.produtoGerente, name='produtoGerente'),

    path('excluir_produto/<int:id_produto>/', views.excluirProduto, name='excluir_produto'),
    path('excluir_pedido/<int:id_pedido>/', views.excluirPedido, name='excluir_pedido'),
    path('excluir_funcionario/<int:id_funcionario>/', views.excluirFuncionario, name='excluir_funcionario'),
    path('excluir_ingrediente/<int:id_ingrediente>/<int:id_produto>/', views.excluirIngrediente, name='excluir_ingrediente'),

    path('attProduto/<int:id_produto>/', views.attProduto, name='attProduto'),

    # FUNÇÕES DE DADOS #
    path('dados_funcionario/', views.dados_funcionario, name='dados_funcionario'),
    path('dados_produto/', views.dadosProduto, name='dados_produto'),
    path('dados_pedido/', views.dadosPedido, name='dados_pedido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)