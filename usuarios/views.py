import json
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as logout_django
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import Usuario
from gerenciamento.models import EnderecoEntrega, Pedido, PedidoProduto, Produto
import re
import datetime
from django.db import transaction

@login_required(login_url='/usuarios/cadastro/')
def principal(request):
    produtos_list = Produto.objects.all()
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    ingredientes_produto = {}
    for produto in produtos_list:
        ingredientes_produto[produto.id_produto] = produto.ingredientes.all()

    contexto = {'pedido':pedido ,'produtos': produtos_list, 'itens': itens, 'carrinho_itens': carrinho_itens, 'ingredientes_produto': ingredientes_produto}
    return render(request, 'principal.html', contexto)

@login_required(login_url='/usuarios/cadastro/')
def carrinho(request):
    
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    contexto = {'pedido':pedido , 'itens': itens, 'carrinho_itens': carrinho_itens}
    return render(request, 'carrinho.html', contexto)

@login_required(login_url='/usuarios/cadastro/')
def checkout(request):
    
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    contexto = {'pedido':pedido , 'itens': itens, 'carrinho_itens': carrinho_itens}
    return render(request, 'checkout.html', contexto)

def cadastro(request):
    if request.method == 'GET':
        usuarios_list = Usuario.objects.all()
        return render(request, 'cadastro.html', {'usuarios': usuarios_list})
    elif request.method == 'POST':
        username = request.POST.get('email')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        email = request.POST.get('email')
        password = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        permissao = False

        user = Usuario.objects.filter(cpf=cpf)
        user = Usuario.objects.filter(email=email)

        if user.exists():
            return render(request, 'cadastro.html', {'nome': username, 'sobrenome':sobrenome, 'telefone': telefone, 'endereco': endereco, 'permissao': permissao, 'erro': 'Usuário já cadastrado!'})
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'cadastro.html', {'nome': username, 'sobrenome':sobrenome, 'telefone': telefone, 'endereco': endereco, 'cpf': cpf, 'permissao': permissao, 'erro': 'E-mail inválido!'})
        
        usuario = Usuario.objects.create(username=username, first_name=nome, last_name=sobrenome, cpf=cpf, telefone=telefone, endereco=endereco, email=email, password=password, permissao=permissao)
        print(username, nome, sobrenome, cpf, email, password, telefone, endereco, permissao)
        usuario.save()
        return HttpResponse('Usuário cadastrado com sucesso!')
    else:
        return render(request, 'cadastro.html')

def login(request):
    if request.method == 'POST':
        usuarios_list = Usuario.objects.all()
        print(usuarios_list)
        emailInserido = request.POST.get('email')
        passwordInserida = request.POST.get('senha')

        for usuario in usuarios_list:
            if usuario.email == emailInserido and usuario.password == passwordInserida:
                login_django(request, usuario)
                # Usuário encontrado, autenticação bem-sucedida
                print('Usuário autenticado com sucesso!')
                # Faça qualquer ação adicional necessária
                return redirect('principal')
        else:
            # Loop concluído sem encontrar um usuário correspondente
            print('Falha na autenticação!')

    return render(request, 'cadastro.html')

@login_required(login_url='/usuarios/cadastro/')
def pesquisar_produto(request):
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user, data=datetime.datetime.now() , completo=False)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens
    else:
        itens = []
        carrinho_itens = {'get_carrinho_total': 0, 'get_carrinho_itens': 0}

    termo_pesquisa = request.GET.get('Pesquisar', '')
    resultados = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)
    contexto = {'pedido':pedido , 'itens': itens, 'carrinho_itens': carrinho_itens, 'resultados': resultados, 'termo_pesquisa': termo_pesquisa}
    return render(request, 'pesquisarProduto.html', contexto)
        
@login_required(login_url='/usuarios/cadastro/')
def logout(request):
    # Exclui o pedido atual do usuário, se existir e não estiver completo
    if request.user.is_authenticated:
        pedido_incompleto = Pedido.objects.filter(cliente=request.user, completo=False).first()
        if pedido_incompleto:
            pedido_incompleto.delete()

    # Realiza o logout do usuário
    logout_django(request)
    
    # Redireciona para a página de login
    return redirect('/usuarios/cadastro/')

@login_required(login_url='/usuarios/cadastro/')
def perfil(request):
    if request.method == 'POST':
        user = request.user
        user.nome = request.POST.get('nome')
        user.sobrenome = request.POST.get('sobrenome')
        user.telefone = request.POST.get('telefone')
        user.endereco = request.POST.get('endereco')
        user.email = request.POST.get('email')
        user.password = (request.POST.get('senha'))
        user.username = (request.POST.get('nome'))
        user.save()
        return redirect('perfil')
    # Filtra os pedidos do usuário com valor maior que 0
    pedidos = Pedido.objects.filter(cliente=request.user, valor_final__gt=0)
    return render(request, 'perfil.html',{'pedidos': pedidos})

@login_required
def excluirPerfil(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        print('Usuário excluído com sucesso!')
        return render(request, 'cadastro.html')

@transaction.atomic
def updateItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_produto = data['id_produto']
        action = data['action']

        print('Action:', action)
        print('Produto:', id_produto)

        cliente = request.user
        produto = Produto.objects.get(id_produto=id_produto)
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, completo=False)

        pedido_produto, criado = PedidoProduto.objects.get_or_create(pedido=pedido, produto=produto)

        if action == 'add':
            pedido_produto.quantidade_comprada = (pedido_produto.quantidade_comprada + 1)
        elif action == 'remove':
            pedido_produto.quantidade_comprada = (pedido_produto.quantidade_comprada - 1)
        
        pedido_produto.save()

        if pedido_produto.quantidade_comprada <= 0:
            pedido_produto.delete()

        return JsonResponse('Item adicionado', safe=False)

@csrf_exempt
def processaPedido(request):
    id_transacao = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        cliente = request.user
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        pedido.valor_final = float(data['form']['total'].replace(',', '.'))
        pedido.id_transacao = id_transacao

        if pedido.valor_final == pedido.get_carrinho_total:
            pedido.completo = True
        pedido.save()

        enderecoEntrega = EnderecoEntrega.objects.create(
            usuario=cliente,
            pedido=pedido,
            endereco=data['form']['endereco'],
            bairro=data['form']['bairro'],
            cidade=data['form']['cidade'],
            estado=data['form']['estado'],
        )
        enderecoEntrega.save()

    else:
        print('Usuário não está logado')

    return JsonResponse('Pedido processado', safe=False)
