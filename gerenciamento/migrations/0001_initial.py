# Generated by Django 5.0.1 on 2024-01-17 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('cpf', models.CharField(max_length=11)),
                ('telefone', models.CharField(max_length=20)),
                ('cargo', models.CharField(max_length=255)),
                ('salario', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('unidadeMedida', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=255)),
                ('preco', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PedidoProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.FloatField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.pedido')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.produto')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='produtos',
            field=models.ManyToManyField(through='gerenciamento.PedidoProduto', to='gerenciamento.produto'),
        ),
        migrations.CreateModel(
            name='ProdutoIngrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.FloatField()),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.ingrediente')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gerenciamento.produto')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='ingredientes',
            field=models.ManyToManyField(through='gerenciamento.ProdutoIngrediente', to='gerenciamento.ingrediente'),
        ),
    ]
