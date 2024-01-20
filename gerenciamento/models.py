from django.db import models
from usuarios import models as usuarios_models

class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nome_ingrediente = models.CharField(max_length=255)
    unidade_Medida = models.CharField(max_length=255)    

    def __str__(self) -> str:
        return f'Nome: {self.nome} | Unidade de Medida: {self.unidadeMedida}'

class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ('doce', 'Doce'),
        ('salgado', 'Salgado'),
        ('bebida', 'Bebida'),
        ('bolo', 'Bolo')
    ]

    id_produto = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    preco = models.FloatField()
    ingredientes = models.ManyToManyField(Ingrediente, through='ProdutoIngrediente')
    categoria = models.CharField(max_length=15, choices=CATEGORIA_CHOICES, default='salgado')
    imagem = models.ImageField(upload_to='media/', null=True, blank=True)

    

class ProdutoIngrediente(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade_usada = models.FloatField()

class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome_funcionario = models.CharField(max_length=255)
    telefone_funcionario = models.CharField(max_length=20)
    cargo = models.CharField(max_length=255)
    salario = models.FloatField()

    def __str__(self) -> str:
        return f'Nome: {self.nome_funcionario} | Telefone: {self.telefone_funcionario} | Cargo: {self.cargo} | Salário: {self.salario}'

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(usuarios_models.Usuario, on_delete=models.CASCADE, default=1)
    data = models.DateField()
    valor_final = models.FloatField()
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
    quantidade_comprada = models.FloatField()



