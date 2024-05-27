# Generated by Django 5.0.6 on 2024-05-27 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0002_alter_utente_datanascita_alter_utente_piva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartacredito',
            name='scadenza',
        ),
        migrations.AddField(
            model_name='cartacredito',
            name='scadenzaAnno',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cartacredito',
            name='scadenzaMese',
            field=models.IntegerField(default=1),
        ),
    ]
