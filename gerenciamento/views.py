from django.utils import timezone
import datetime
import json
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from gerenciamento.forms import ProdutoForm
from fpdf import FPDF
from io import BytesIO

from gerenciamento.models import Funcionario, Ingrediente, Pedido, PedidoProduto, Produto, ProdutoIngrediente, Avaliacao
from usuarios.models import Usuario

def verifica_permissao(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.permissao:
            return func(request, *args, **kwargs)
        else:
            return redirect('cadastro')
    return wrapper

#telas

def principalGerente(request):
    if request.user.is_authenticated and request.user.permissao:
        produtos_list = Produto.objects.all()
        return render(request, 'principalGerente.html', {'produtos': produtos_list})
    else:
        return redirect('cadastro')

@verifica_permissao
def lista_pedidos(request):
     # Obtém a data do primeiro dia do mês atual
    primeiro_dia_mes_atual = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Obtém todos os pedidos do mês atual
    pedidos_mes_atual = Pedido.objects.filter(data__gte=primeiro_dia_mes_atual)

    # Calcula a soma do valor de todos os pedidos do mês atual
    soma_valor_pedidos_mes_atual = sum(pedido.valor_final for pedido in pedidos_mes_atual)
    pedidos_list = Pedido.objects.order_by('-id_pedido')
    return render(request, 'listarPedidos.html', {'pedidos': pedidos_list, 'soma_valor_pedidos_mes_atual': soma_valor_pedidos_mes_atual})

@verifica_permissao
def clientes(request):
    if request.method == "GET":
        clientes_list = Usuario.objects.order_by('-date_joined')
        return render(request, 'clientes.html', {'clientes': clientes_list})
    else:
        return render(request, 'clientes.html')

@verifica_permissao
def funcionarios(request):
    funcionarios_list = Funcionario.objects.all()
    return render(request, 'funcionarios.html', {'funcionarios': funcionarios_list})

@verifica_permissao
def perfil(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('nome')
        user.last_name = request.POST.get('sobrenome')
        user.telefone = request.POST.get('telefone')
        user.endereco = request.POST.get('endereco')
        user.email = request.POST.get('email')
        user.password = (request.POST.get('senha'))
        user.username = (request.POST.get('nome'))
        user.permissao = True
        user.save()
        return redirect('perfilGerente.html')
    return render(request, 'perfilGerente.html')
    

def excluirPerfil(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        print('Usuário excluído com sucesso!')
        return render(request, 'cadastro.html')


    
#funções de adicionar

@verifica_permissao
def addFuncionario(request):
    funcionarios_list = Funcionario.objects.all()
    if request.method == "GET":
        return render(request, 'funcionarios.html', {'funcionarios': funcionarios_list})
    elif request.method == "POST":
        nome_funcionario = request.POST.get('nome_funcionario')
        telefone_funcionario = request.POST.get('telefone_funcionario')
        cargo = request.POST.get('cargo')
        salario = request.POST.get('salario')

        funcionario = Funcionario.objects.filter(nome_funcionario=nome_funcionario, telefone_funcionario=telefone_funcionario, cargo=cargo, salario=salario)

        if funcionario:
            return JsonResponse({'status': '500'})
        else:
            funcionario = Funcionario.objects.create(nome_funcionario=nome_funcionario, telefone_funcionario=telefone_funcionario, cargo=cargo, salario=salario)
            funcionario.save()

        return render(request, 'funcionarios.html', {'funcionarios': funcionarios_list})
    

@verifica_permissao  
def addProduto(request):
    categorias = Produto.CATEGORIA_CHOICES
    if request.method == 'POST':
        nome_produto = request.POST.get('nome_produto')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        categoria = request.POST.get('categoria')
        imagem = request.FILES.get('imagem')
        nomeIngredientes = request.POST.getlist('nome_ingrediente')
        unidadeMedidas = request.POST.getlist('unidade_Medida')

        # Salvando os dados do produto no banco de dados
        produto = Produto.objects.create(nome_produto=nome_produto, descricao=descricao, preco=preco, categoria=categoria, imagem=imagem)
        produto.save()
        print(produto)

        for nomeIngrediente, unidadeMedida in zip(nomeIngredientes, unidadeMedidas):
            ingrediente, created = Ingrediente.objects.get_or_create(nome_ingrediente=nomeIngrediente, unidade_Medida=unidadeMedida)
            produto_ingrediente = ProdutoIngrediente.objects.create(produto=produto, ingrediente=ingrediente)
            produto_ingrediente.save()
            print(ingrediente)

        # Redirecionar para alguma página de sucesso ou para a página inicial
        return redirect('principalGerente')

    # Se o método da requisição não for POST, renderizar o formulário vazio
    return render(request, 'adicionarProduto.html', {'categorias': categorias})

@verifica_permissao       
def produtoGerente(request, id_produto):
    categorias = Produto.CATEGORIA_CHOICES
    produto = get_object_or_404(Produto, id_produto=id_produto)
    media_avaliacoes = Avaliacao.calcular_media_avaliacoes(produto)
    ingredientes_produto = produto.ingredientes.all()

    avaliacoes = Avaliacao.objects.filter(produto=produto) 

    contexto = {'produto': produto,  'avaliacoes': avaliacoes, 'media_avaliacoes': media_avaliacoes, 'ingredientes_produto': ingredientes_produto, 'categorias': categorias}
    return render(request, 'produtoGerente.html', contexto)
        
# FUNÇÕES DE BUSCA
@verifica_permissao
def buscar_sugestoes(request):
    termo_pesquisa = request.GET.get('termo', '')
    sugestoes = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)[:5]

    sugestoes_data = [{'nome': produto.nome_produto, 'preco': produto.preco, 'imagem_url': produto.imagem.url} for produto in sugestoes]
    return JsonResponse({'sugestoes': sugestoes_data})

@verifica_permissao
def pesquisarProdutoGerente(request):
    termo_pesquisa = request.GET.get('Pesquisar', '')
    resultados = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)
    contexto = {'resultados': resultados, 'termo_pesquisa': termo_pesquisa}
    return render(request, 'pesquisaProdutoGerente.html', contexto)

#funções de atualizar
@verifica_permissao
def attProduto(request, id_produto):
    if request.method == 'POST':
        produtoAtt = Produto.objects.get(id_produto=id_produto)
        print(produtoAtt)
        produtoAtt.nome_produto = request.POST.get('nome_produto')
        produtoAtt.descricao = request.POST.get('descricao')
        produtoAtt.preco = request.POST.get('preco')
        produtoAtt.categoria = request.POST.get('categoria')
        produtoAtt.save()

        ProdutoIngrediente.objects.filter(produto=produtoAtt).delete()

        nomeIngredientes = request.POST.getlist('nome_ingrediente')
        unidadeMedidas = request.POST.getlist('unidade_Medida')

        for nomeIngrediente, unidadeMedida in zip(nomeIngredientes, unidadeMedidas):
            ingrediente, created = Ingrediente.objects.get_or_create(nome_ingrediente=nomeIngrediente, unidade_Medida=unidadeMedida)
            produto_ingrediente = ProdutoIngrediente.objects.create(produto=produtoAtt, ingrediente=ingrediente)
            produto_ingrediente.save()
            print(ingrediente)

        return redirect('produtoGerente', id_produto=id_produto)
    
    return redirect('produtoGerente', id_produto=id_produto)

def attPedido(request):
    pass

@verifica_permissao
def attFuncionario(request):
    if request.method == 'POST':
        id_funcionario = request.POST.get('id_funcionario')
        print(id_funcionario)
        funcionarioAtt = Funcionario.objects.get(id_funcionario=id_funcionario)
        print(funcionarioAtt)
        funcionarioAtt.nome_funcionario = request.POST.get('nome_funcionario')
        funcionarioAtt.telefone_funcionario = request.POST.get('telefone_funcionario')
        funcionarioAtt.cargo = request.POST.get('cargo')
        funcionarioAtt.salario = request.POST.get('salario')
        print(funcionarioAtt)
        funcionarioAtt.save()
        return redirect('funcionarios')
    return redirect('funcionarios')
    
#funções de deletar
    
@verifica_permissao
def excluirProduto(request, id_produto):
    produto = Produto.objects.get(id_produto=id_produto)
    print(produto)
    produto.delete()
    return redirect('principalGerente')

@verifica_permissao
def excluirPedido(request, id_pedido):
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    print(pedido)
    pedido.delete()
    return redirect('listaPedidos')

@verifica_permissao
def excluirFuncionario(request, id_funcionario):
    funcionario = Funcionario.objects.get(id_funcionario=id_funcionario)
    print(funcionario)
    funcionario.delete()
    return redirect('funcionarios')

@verifica_permissao
def excluirIngrediente(request, id_ingrediente, id_produto):
    produto = Produto.objects.get(id_produto=id_produto)
    ingrediente = Ingrediente.objects.get(id_ingrediente=id_ingrediente)
    produto_ingrediente = ProdutoIngrediente.objects.get(produto=produto, ingrediente=ingrediente)
    produto_ingrediente.delete()
    return redirect('produtoGerente', id_produto=id_produto)

#funções de dados

@verifica_permissao
def dadosPedido(request):
    id_pedido = request.POST.get('id_pedido')
    pedido = Pedido.objects.filter(id_pedido=id_pedido)
    pedido_json = json.loads(serializers.serialize('json', pedido))[0]['fields']
    pedido_id = json.loads(serializers.serialize('json', pedido))[0]['pk']
    data = {'pedido': pedido_json, 'pedido_id': pedido_id}
    return JsonResponse(data)

@verifica_permissao
def dadosProduto(request):
    id_produto = request.POST.get('id_produto')
    produto = Produto.objects.filter(id_produto=id_produto).first()
    print(produto)
    if produto:
        # Obtém todos os ingredientes associados ao produto
        ingredientes = produto.get_ingredientes
        
        # Serializa os ingredientes manualmente para um formato JSON válido
        ingredientes_json = [
            {
                'id_ingrediente': ingrediente.id_ingrediente,
                'nome_ingrediente': ingrediente.nome_ingrediente,
                'unidade_Medida': ingrediente.unidade_Medida,
            }
            for ingrediente in ingredientes
        ]
        
        # Retorna a lista de ingredientes como resposta JSON
        return JsonResponse({'ingredientes': ingredientes_json, 'id_produto':produto.id_produto})
    else:
        # Se o produto não for encontrado, retorna uma resposta de erro
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)

@verifica_permissao
def dados_funcionario(request):
    if request.method == "POST":
        id_funcionario = request.POST.get('id_funcionario')
        print(id_funcionario)
        funcionario = Funcionario.objects.filter(id_funcionario=id_funcionario).first()  # Use .first() para obter apenas um objeto
        if funcionario:
            data = {
                'id_funcionario': funcionario.id_funcionario,
                'nome_funcionario': funcionario.nome_funcionario,
                'telefone_funcionario': funcionario.telefone_funcionario,
                'cargo': funcionario.cargo,
                'salario': funcionario.salario,
            }
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Funcionário não encontrado'}, status=404)
        
def dados_perfil(request):
    if request.method == "POST":
        user = request.user
        data = {
            'nome': user.first_name,
            'sobrenome': user.last_name,
            'telefone': user.telefone,
            'endereco': user.endereco,
            'email': user.email,
            'senha': user.password,
        }
        print(data)
        return JsonResponse(data)

#detalhes de pedido


def notaPedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(35, 10, 'Cliente: ', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{pedido.cliente.first_name} {pedido.cliente.last_name}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Data da Compra: ', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{pedido.data}', 1, 1, 'L', 1)

    pdf.cell(35, 10, 'Produtos: ', 1, 0, 'L', 1)

    pedido_produtos = PedidoProduto.objects.filter(pedido=pedido)
    for i, pedido_produto in enumerate(pedido_produtos):
        produto = pedido_produto.produto
        quantidade = pedido_produto.quantidade_comprada

        pdf.cell(0, 10, f'{produto.nome_produto} - Quantidade: {quantidade} - Preço: R${produto.preco}', 1, 1, 'L', 1)
        if not i == len(pedido_produtos) - 1:
            pdf.cell(35, 10, '', 0, 0, 'L', 0)

    pdf.cell(35, 10, 'Valor Total: ', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'R${pedido.get_carrinho_total}', 1, 1, 'L', 1)
    
    pdf_content = pdf.output(dest='S').encode('latin-1')
    pdf_bytes = BytesIO(pdf_content)

    return FileResponse(pdf_bytes, as_attachment=True, filename='notaPedido.pdf')

