from django.db import models
from usuarios import models as usuarios_models

class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nome_ingrediente = models.CharField(max_length=255)
    unidade_Medida = models.CharField(max_length=255)    

    def __str__(self) -> str:
        return f'ID: {self.id_ingrediente} | Nome: {self.nome_ingrediente} | Unidade de Medida: {self.unidade_Medida}'
    
class Like(models.Model):
    usuario = models.ForeignKey(usuarios_models.Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE, related_name='likes')

    def __str__(self) -> str:
        return f'Usuario: {self.usuario.username} | Produto: {self.produto.nome_produto}'

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

    def __str__(self) -> str:
        return f'ID: {self.id_produto} | Nome: {self.nome_produto} | Descrição: {self.descricao} | Preço: {self.preco} | Categoria: {self.categoria}'
    
    @property
    def numero_likes(self):
        return self.likes.count()
    
    @property
    def imageURL(self):
        try:
            url = self.imagem.url
        except:
            url = ''
        return url
    
    @property
    def get_ingredientes(self):
        ingredientes_produto = self.produtoingrediente_set.all()
        ingredientes = [item.ingrediente for item in ingredientes_produto]
        return ingredientes

class ProdutoIngrediente(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade_usada = models.FloatField()

    def __str__(self) -> str:
        return f'Produto: {self.produto.nome_produto} | Ingrediente: {self.ingrediente.nome_ingrediente} | Quantidade: {self.quantidade_usada}'

class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome_funcionario = models.CharField(max_length=255)
    telefone_funcionario = models.CharField(max_length=20)
    cargo = models.CharField(max_length=255)
    salario = models.FloatField()

    def __str__(self) -> str:
        return f'ID: {self.id_funcionario} Nome: {self.nome_funcionario} | Telefone: {self.telefone_funcionario} | Cargo: {self.cargo} | Salário: {self.salario}'

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_transacao = models.CharField(max_length=255, null=True)
    cliente = models.ForeignKey(usuarios_models.Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateField(auto_now_add=True)
    valor_final = models.FloatField(default=0.0)
    produtos = models.ManyToManyField(Produto, through='PedidoProduto')
    completo = models.BooleanField(default=False, null=True, blank=False)

    def precoTotal(self):
        total = float(0)
        for produto in self.produtos.all():
            total += produto.preco

        return total
    
    def __str__(self) -> str:
        return f'ID: {self.id_pedido} | Cliente: {self.cliente} | Data: {self.data} | Valor Final: {self.valor_final}'
    
    @property
    def get_carrinho_total(self):
        pedido_produtos = self.pedidoproduto_set.all()
        total = sum([item.get_total for item in pedido_produtos])
        return total
    
    @property
    def get_carrinho_itens(self):
        pedido_produtos = self.pedidoproduto_set.all()
        total = sum([item.quantidade_comprada for item in pedido_produtos])
        return total

class EnderecoEntrega(models.Model):
    usuario = models.ForeignKey(usuarios_models.Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.endereco
    

class PedidoProduto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_comprada = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self) -> str:
        return f'Pedido: {self.pedido.id_pedido} | Produto: {self.produto.nome_produto} | Quantidade: {self.quantidade_comprada}'
    
    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade_comprada
        return total



