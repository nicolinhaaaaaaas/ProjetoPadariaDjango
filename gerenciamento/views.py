from django.shortcuts import render

def principalGerente(request):
    return render(request, 'principalGerente.html')

def lista_pedidos(request):
    return render(request, 'listarPedidos.html')

def clientes(request):
    return render(request, 'clientes.html')

def funcionarios(request):
    return render(request, 'funcionarios.html')

def perfil(request):
    return render(request, 'perfilGerente.html')

def addProduto(request):
    return render(request, 'adicionarProduto.html')

def pedido(request):
    pass

def attPedido(request):
    pass

def gerenciamento(request):
    pass

def addFuncionario(request):
    pass

def attProduto(request):
    pass

def attFuncionario(request):
    pass

def notaPedido(request):
    pass