# Generated by Django 5.0.1 on 2024-01-19 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0003_rename_cpf_funcionario_cpf_funcionario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='cpf_funcionario',
        ),
    ]