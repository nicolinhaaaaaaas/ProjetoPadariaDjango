from django.db import models
from usuarios import models as usuarios_models

class Ingrediente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    unidadeMedida = models.CharField(max_length=255)    

    def __str__(self) -> str:
        return f'Nome: {self.nome} | Unidade de Medida: {self.unidadeMedida}'

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    preco = models.FloatField()
    ingredientes = models.ManyToManyField(Ingrediente, through='ProdutoIngrediente')

    def __str__(self) -> str:
        return f'Nome: {self.nome} | Descrição: {self.descricao} | Preço: {self.preco}'

class ProdutoIngrediente(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.FloatField()

class Funcionario(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=20)
    cargo = models.CharField(max_length=255)
    salario = models.FloatField()

    def __str__(self) -> str:
        return f'Nome: {self.nome} | CPF: {self.cpf} | Telefone: {self.telefone} | Cargo: {self.cargo} | Salário: {self.salario}'

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(usuarios_models.Usuario, on_delete=models.CASCADE, default=1)
    data = models.DateField()
    hora = models.TimeField()
    valor = models.FloatField()
    produtos = models.ManyToManyField(Produto, through='PedidoProduto')

    def precoTotal(self):
        total = float(0)
        for produto in self.produtos.all():
            total += produto.preco

        return total

    def __str__(self) -> str:
        return f'Cliente: {self.cliente} | Data: {self.data} | Hora: {self.hora} | Valor: {self.valor}'
    

class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.FloatField()



