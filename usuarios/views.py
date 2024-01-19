from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import Usuario
from gerenciamento.models import Pedido
import re


def principal(request):
    return render(request, 'principal.html')

def cadastro(request):
    if request.method == 'GET':
        usuarios_list = Usuario.objects.all()
        return render(request, 'cadastro.html', {'usuarios': usuarios_list})
    elif request.method == 'POST':
        username = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        permissao = False

        user = Usuario.objects.filter(cpf=cpf)
        user = Usuario.objects.filter(email=email)

        if user.exists():
            return render(request, 'cadastro.html', {'nome': username, 'telefone': telefone, 'endereco': endereco, 'permissao': permissao, 'erro': 'Usuário já cadastrado!'})
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'cadastro.html', {'nome': username, 'telefone': telefone, 'endereco': endereco, 'cpf': cpf, 'permissao': permissao, 'erro': 'E-mail inválido!'})
        
        usuario = Usuario.objects.create(username=username, cpf=cpf, telefone=telefone, endereco=endereco, email=email, password=password, permissao=permissao)
        print(username, cpf, email, password, telefone, endereco, permissao)
        usuario.save()
        return HttpResponse('Usuário cadastrado com sucesso!')
    else:
        return render(request, 'cadastro.html')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        user = authenticate(request, cpf=cpf, password=senha)
        if user is not None:
            login_django(request, user)
            return HttpResponse('Usuário logado com sucesso!')
        else:
            print(cpf, senha)
            return HttpResponse('Usuário ou senha incorretos!')
        
#@login_required
def logout(request):
    logout(request)
    return HttpResponse('Usuário deslogado com sucesso!')

#@login_required(login_url='/usuarios/login/')
def perfil(request):
    return render(request, 'perfil.html')

#@login_required
def atualizarPerfil(request):
    if request.method == 'POST':
        pass

#@login_required
def excluirPerfil():
    pass

#@login_required
def pedidosProprios():
    pass   

#@login_required
def fazerPedido():
    pass

def pedidos(request, id):
   pedido = get_object_or_404(Pedido, id=id)
   return render(request, 'pedidos.html', {'pedido': pedido})