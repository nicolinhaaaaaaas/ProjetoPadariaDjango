from django.urls import path
from . import views

urlpatterns = [
    path('', views.principalGerente, name='gerenciamento'),
    path('perfilGerente/', views.perfil, name='perfilGerente'),
    path('principalGerente/', views.principalGerente, name='principalGerente'),
    path('listaPedidos/', views.lista_pedidos, name='listaPedidos'),
    path('pedido/<int:id_pedido>', views.pedido, name='pedido'),
    path('funcionarios/', views.funcionarios, name='funcionarios'),
    path('addFuncionario/', views.addFuncionario, name='addFuncionario'),
    path('updateFuncionario/<int:id_funcionario>', views.attFuncionario, name='updateFuncionario'),
    path('addProduto/', views.addProduto, name='addProduto'),
    path('clientes/' , views.clientes, name='clientes'),
]