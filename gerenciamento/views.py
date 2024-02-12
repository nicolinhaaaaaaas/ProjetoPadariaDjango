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

#telas
def principalGerente(request):
    produtos_list = Produto.objects.all()
    return render(request, 'principalGerente.html', {'produtos': produtos_list})

def lista_pedidos(request):
    pedidos_list = Pedido.objects.order_by('-data')
    return render(request, 'listarPedidos.html', {'pedidos': pedidos_list})

def clientes(request):
    if request.method == "GET":
        clientes_list = Usuario.objects.order_by('-date_joined')
        return render(request, 'clientes.html', {'clientes': clientes_list})
    else:
        return render(request, 'clientes.html')

def funcionarios(request):
    funcionarios_list = Funcionario.objects.all()
    return render(request, 'funcionarios.html', {'funcionarios': funcionarios_list})

def perfil(request):
    return render(request, 'perfilGerente.html')


    
#funções de adicionar
    
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
    
def addProduto(request):
    if request.method == "GET":
        form = ProdutoForm()
        produtos_list = Produto.objects.all()
        return render(request, 'adicionarProduto.html', {'form': form, 'produtos': produtos_list})
    elif request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            
            nome_ingredientes = request.POST.getlist('nome_ingrediente')
            unidadeMedidas = request.POST.getlist('unidadeMedida')
            quantidades = request.POST.getlist('quantidade')

            for nome_ingrediente, unidadeMedida, quantidade in zip(nome_ingredientes, unidadeMedidas, quantidades):
                try:
                    ingrediente = Ingrediente.objects.get(nome_ingrediente=nome_ingrediente)
                except Ingrediente.DoesNotExist:
                    ingrediente = Ingrediente.objects.create(nome_ingrediente=nome_ingrediente, unidadeMedida=unidadeMedida)
                    ingrediente.save()
                
                produtoIng = ProdutoIngrediente.objects.create(produto=produto, ingrediente=ingrediente, quantidade_usada=quantidade)
                
                produtoIng.save()
            
            return redirect('lista_produtos')  # Redireciona para a lista de produtos após adicionar com sucesso
        else:
            # Se o formulário não for válido, você pode querer lidar com isso de acordo com seus requisitos
            return render(request, 'adicionarProduto.html', {'form': form})
        
def produtoGerente(request, id_produto):
    produto = get_object_or_404(Produto, id_produto=id_produto)
    media_avaliacoes = Avaliacao.calcular_media_avaliacoes(produto)
    ingredientes_produto = produto.ingredientes.all()

    avaliacoes = Avaliacao.objects.filter(produto=produto) 

    contexto = {'produto': produto,  'avaliacoes': avaliacoes, 'media_avaliacoes': media_avaliacoes, 'ingredientes_produto': ingredientes_produto}
    return render(request, 'produtoGerente.html', contexto)
        
# FUNÇÕES DE BUSCA
def buscar_sugestoes(request):
    termo_pesquisa = request.GET.get('termo', '')
    sugestoes = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)[:5]

    sugestoes_data = [{'nome': produto.nome_produto, 'preco': produto.preco, 'imagem_url': produto.imagem.url} for produto in sugestoes]
    return JsonResponse({'sugestoes': sugestoes_data})

def pesquisarProdutoGerente(request):
    termo_pesquisa = request.GET.get('Pesquisar', '')
    resultados = Produto.objects.filter(nome_produto__icontains=termo_pesquisa)
    contexto = {'resultados': resultados, 'termo_pesquisa': termo_pesquisa}
    return render(request, 'pesquisaProdutoGerente.html', contexto)

#funções de atualizar
def attProduto(request):
    pass

def attPedido(request):
    pass

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
    
#funções de deletar
    
def excluirProduto(request):
    pass

def excluirPedido(request):
    pass

def excluirFuncionario(request, id):
    funcionario = get_object_or_404(Funcionario)

    if request.method == 'POST':
        # Se a solicitação é um POST, exclua o funcionário
        funcionario.delete()
        return redirect('lista_funcionarios')  # Redirecione para a página de lista de funcionários após a exclusão

    return render(request, 'excluir_funcionario.html', {'funcionario': funcionario})

#funções de dados

def dadosPedido(request):
    id_pedido = request.POST.get('id_pedido')
    pedido = Pedido.objects.filter(id_pedido=id_pedido)
    pedido_json = json.loads(serializers.serialize('json', pedido))[0]['fields']
    pedido_id = json.loads(serializers.serialize('json', pedido))[0]['pk']
    data = {'pedido': pedido_json, 'pedido_id': pedido_id}
    return JsonResponse(data)

def dadosProduto(request):
    id_produto = request.POST.get('id_produto')
    produto = Produto.objects.filter(id_produto=id_produto)
    ingredientes = ProdutoIngrediente.objects.filter(produto=produto[0])

    produto_json = json.loads(serializers.serialize('json', produto))[0]['fields']
    produto_id = json.loads(serializers.serialize('json', produto))[0]['pk']

    ingredientes_json = json.loads(serializers.serialize('json', ingredientes))
    ingredientes_json = [{'fields': i['fields'], 'id': i['pk']} for i in ingredientes_json]
    print(ingredientes_json)
    data = {'produto': produto_json, 'produto_id': produto_id, 'ingredientes': ingredientes_json}
    return JsonResponse(data)

def dadosFuncionario(request):
    if request.method == "POST":
        id_funcionario = request.POST.get('id_funcionario')
        print("ID do funcionário:", id_funcionario)

        funcionario = Funcionario.objects.filter(id_funcionario=id_funcionario).first()  # Use .first() para obter o primeiro objeto ou None se não houver nenhum
        if funcionario:
            funcionario_json = json.loads(serializers.serialize('json', [funcionario]))[0]['fields']
            funcionario_id = funcionario.pk
            data = {'funcionario': funcionario_json, 'funcionario_id': funcionario_id}
            print(data)
            return JsonResponse(data)
        else:
            # Retorna um erro ou uma resposta vazia, dependendo do que você quer fazer
            return HttpResponse(status=404)  # Por exemplo, pode retornar um erro 404 se o funcionário não for encontrado


#detalhes de pedido

def pedido(request):
    pass

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

