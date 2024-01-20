# forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome_produto', 'descricao', 'preco', 'ingredientes', 'categoria', 'imagem']
        submit = forms.CharField(widget=forms.TextInput(attrs={'type': 'submit', 'value': 'Enviar'}))
