import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from gerenciamento.models import Funcionario, Ingrediente, Produto, ProdutoIngrediente
from usuarios.models import Usuario

def principalGerente(request):
    return render(request, 'principalGerente.html')

def lista_pedidos(request):
    return render(request, 'listarPedidos.html')

def clientes(request):
    if request.method == "GET":
        clientes_list = Usuario.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    else:
        return render(request, 'clientes.html')

def funcionarios(request):
    funcionarios_list = Funcionario.objects.all()
    return render(request, 'funcionarios.html', {'funcionarios': funcionarios_list})

def perfil(request):
    return render(request, 'perfilGerente.html')

def addProduto(request):
    if request.method == "GET":
        produtos_list = Produto.objects.all()
        return render(request, 'adicionarProduto.html', {'produtos': produtos_list})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        preco = request.POST.get('preco')
        descricao = request.POST.get('descricao')

        nome_ingredientes = request.POST.getlist('nome_ingrediente')
        unidadeMedidas = request.POST.getlist('unidadeMedida')
        quantidades = request.POST.getlist('quantidade')

        produto = Produto.objects.create(nome_produto=nome, preco=preco, descricao=descricao)
        
        produto.save()

        for nome_ingrediente, unidadeMedida, quantidade in zip(nome_ingredientes, unidadeMedidas, quantidades):
            try:
                ingrediente = Ingrediente.objects.get(nome_ingrediente=nome_ingrediente)
            except Ingrediente.DoesNotExist:
                ingrediente = Ingrediente.objects.create(nome_ingrediente=nome_ingrediente, unidadeMedida=unidadeMedida)
                ingrediente.save()
            
            produtoIng = ProdutoIngrediente.objects.create(produto=produto, ingrediente=ingrediente, quantidade_usada=quantidade)
            
            produtoIng.save()
        
        return HttpResponse('Produto adicionado com sucesso!')

def attProduto(request):
    pass

def pedido(request):
    pass

def attPedido(request):
    pass

def gerenciamento(request):
    pass

def addFuncionario(request):
    if request.method == "GET":
        funcionarios_list = Funcionario.objects.all()
        return render(request, 'funcionarios.html', {'funcionarios': funcionarios_list})
    elif request.method == "POST":
        nome_funcionario = request.POST.get('nome_funcionario')
        telefone_funcionario = request.POST.get('telefone_funcionario')
        cargo = request.POST.get('cargo')
        salario = request.POST.get('salario')

        funcionario = Funcionario.objects.create(nome_funcionario=nome_funcionario, telefone_funcionario=telefone_funcionario, cargo=cargo, salario=salario)
        
        funcionario.save()

        return render(request, 'funcionarios.html')

def attFuncionario(request, id):
    body = json.loads(request.body)

    nome_funcionario = body['nome']
    telefone_funcionario = body['telefone']
    cargo = body['cargo']
    salario = body['salario']

    funcionario = get_object_or_404(Funcionario, id=id)
    try:
        funcionario.nome_funcionario = nome_funcionario
        funcionario.telefone_funcionario = telefone_funcionario
        funcionario.cargo = cargo
        funcionario.salario = salario
        funcionario.save()
        return JsonResponse({'status': '200', 'nome_funcionario': nome_funcionario, 'telefone_funcionario': telefone_funcionario, 'cargo': cargo, 'salario': salario})
    except:
        return JsonResponse({'status': '500'})
    

def notaPedido(request):
    pass