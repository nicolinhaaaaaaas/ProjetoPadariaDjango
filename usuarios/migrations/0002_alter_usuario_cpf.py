# Generated by Django 5.0.1 on 2024-01-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(max_length=11, primary_key=True, serialize=False, unique=True),
        ),
    ]
