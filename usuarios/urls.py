from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios, name='usuarios'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('principal/', views.principal, name='principal'),
]