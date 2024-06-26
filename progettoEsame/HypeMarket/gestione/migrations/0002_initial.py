# Generated by Django 5.0.6 on 2024-06-07 13:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestione', '0001_initial'),
        ('prodotto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='compravendita',
            name='prodotto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mercato', to='prodotto.prodotto'),
        ),
        migrations.AddField(
            model_name='compravendita',
            name='taglia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mercato', to='prodotto.taglia'),
        ),
    ]
