# Generated by Django 5.1.5 on 2025-02-03 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_scraper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='imagem',
        ),
        migrations.CreateModel(
            name='ImagemProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_imagem', models.URLField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagens', to='web_scraper.produto')),
            ],
        ),
    ]
