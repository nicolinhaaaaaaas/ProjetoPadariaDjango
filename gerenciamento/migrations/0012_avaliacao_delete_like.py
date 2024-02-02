# Generated by Django 5.0.1 on 2024-02-02 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciamento', '0011_alter_pedidoproduto_quantidade_comprada_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('data', models.DateField(auto_now_add=True)),
                ('nota', models.FloatField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='gerenciamento.produto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]