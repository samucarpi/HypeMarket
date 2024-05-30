# Generated by Django 5.0.6 on 2024-05-30 17:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prodotto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=50)),
                ('immagine', models.CharField(max_length=200)),
                ('idModello', models.CharField(max_length=10)),
                ('dataRilascio', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Taglia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taglia', models.CharField(max_length=5)),
                ('propostaMinore', models.FloatField(blank=True, null=True)),
                ('offertaMaggiore', models.FloatField(blank=True, null=True)),
                ('prodotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taglie', to='prodotto.prodotto')),
            ],
        ),
    ]
