# Generated by Django 5.0.1 on 2024-01-30 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0008_alter_pedido_cliente_enderecoentrega'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='data',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='valor_final',
            field=models.FloatField(default=0.0),
        ),
    ]
