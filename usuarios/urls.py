from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.principal, name='usuarios'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('principal/', views.principal, name='principal'),
    path('pesquisar_produto', views.pesquisar_produto, name='pesquisar_produto'),
    path('logout/', views.logout, name='logout'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('processar_pedido/', views.processaPedido, name='processar_pedido'),
    path('produto/<int:id_produto>/', views.produto, name='produto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)