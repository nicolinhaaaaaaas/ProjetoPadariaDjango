# Generated by Django 5.0.1 on 2024-01-29 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0006_alter_produto_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='id_transacao',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
