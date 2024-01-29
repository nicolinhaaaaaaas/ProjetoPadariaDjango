import json
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from .models import Usuario
from gerenciamento.models import Pedido, PedidoProduto, Produto
import re
import datetime

@login_required(login_url='/usuarios/login/')
def principal(request):
    produtos_list = Produto.objects.all()
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens

    contexto = {'produtos': produtos_list, 'itens': itens, 'carrinho_itens': carrinho_itens}
    return render(request, 'principal.html', contexto)

def carrinho(request):
    
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens

    contexto = {'itens': itens, 'carrinho_itens': carrinho_itens}
    return render(request, 'carrinho.html', contexto)

def checkout(request):
    
    if request.user.is_authenticated:
        pedido, criado = Pedido.objects.get_or_create(cliente=request.user)
        itens = pedido.pedidoproduto_set.all()
        carrinho_itens = pedido.get_carrinho_itens

    contexto = {'itens': itens, 'carrinho_itens': carrinho_itens, 'pedido': pedido}
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

        
def pesquisar_produto(request):
    termo_pesquisa = request.GET.get('Pesquisar', '')
    resultados = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)
    return render(request, 'pesquisarProduto.html', {'resultados': resultados})
        
#@login_required
def logout(request):
    logout(request)
    return HttpResponse('Usuário deslogado com sucesso!')

@login_required(login_url='/usuarios/login/')
def perfil(request):
    pedidos = Pedido.objects.filter(cliente=request.user)
    return render(request, 'perfil.html',{'pedidos': pedidos})

#@login_required
def atualizarPerfil(request):
    if request.method == 'POST':
        pass

#@login_required
def excluirPerfil():
    pass

def adicionarAoCarrinho(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_produto = data.get('id_produto')  # Certifique-se de enviar o ID do produto na solicitação
        quantidade = data.get('quantidade', 1)  # Quantidade padrão é 1 se não for fornecida

        produto = get_object_or_404(Produto, id_produto=id_produto)
        carrinho, criado = Pedido.objects.get_or_create(cliente=request.user)

        # Verifique se o produto já está no carrinho
        pedido_produto, criado = PedidoProduto.objects.get_or_create(pedido=carrinho, produto=produto)

        # Atualize a quantidade se o produto já estiver no carrinho
        if not criado:
            pedido_produto.quantidade_comprada += quantidade
            pedido_produto.save()

        return JsonResponse({'mensagem': 'Produto adicionado ao carrinho com sucesso!'})
    else:
        return JsonResponse({'mensagem': 'Método não permitido.'}, status=405)

def updateItem(request):
    data = json.loads(request.body)
    id_produto = data['id_produto']
    action = data['action']

    print('Action:', action)
    print('Produto:', id_produto)

    cliente = request.user.usuario
    produto = Produto.objects.get(id_produto=id_produto)
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, status='carrinho')

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
        cliente = request.user.usuario
        pedido, criado = Pedido.objects.get_or_create(cliente=cliente)
        total = float(data['form']['total'])
        pedido.id_transacao = id_transacao

        if total == pedido.get_carrinho_total:
            pedido.status = 'Finalizado'
        pedido.save()

    else:
        print('Usuário não está logado')

    return JsonResponse('Pedido processado', safe=False)
