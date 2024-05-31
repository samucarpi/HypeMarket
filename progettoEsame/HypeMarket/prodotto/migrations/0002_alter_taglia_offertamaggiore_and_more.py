# Generated by Django 5.0.6 on 2024-05-31 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0003_initial'),
        ('prodotto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taglia',
            name='offertaMaggiore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taglie', to='gestione.offerta'),
        ),
        migrations.AlterField(
            model_name='taglia',
            name='propostaMinore',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taglie', to='gestione.proposta'),
        ),
    ]