# Generated by Django 5.0.6 on 2024-05-31 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestione', '0002_initial'),
        ('utente', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='compravendita',
            name='utente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mercato', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acquisto',
            name='carta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquisti', to='utente.cartacredito'),
        ),
        migrations.AddField(
            model_name='acquisto',
            name='indirizzoSpedizione',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acquisti', to='utente.indirizzospedizione'),
        ),
        migrations.AddField(
            model_name='offerta',
            name='carta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerte', to='utente.cartacredito'),
        ),
        migrations.AddField(
            model_name='offerta',
            name='indirizzoSpedizione',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offerte', to='utente.indirizzospedizione'),
        ),
        migrations.AddField(
            model_name='proposta',
            name='banca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposte', to='utente.datibancari'),
        ),
        migrations.AddField(
            model_name='proposta',
            name='indirizzoFatturazione',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposte', to='utente.indirizzofatturazione'),
        ),
        migrations.AddField(
            model_name='vendita',
            name='banca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendite', to='utente.datibancari'),
        ),
        migrations.AddField(
            model_name='vendita',
            name='indirizzoFatturazione',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendite', to='utente.indirizzofatturazione'),
        ),
    ]
