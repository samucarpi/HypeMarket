# Generated by Django 5.0.6 on 2024-05-27 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0004_alter_cartacredito_scadenzaanno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartacredito',
            name='scadenzaAnno',
            field=models.CharField(max_length=4),
        ),
        migrations.AlterField(
            model_name='cartacredito',
            name='scadenzaMese',
            field=models.CharField(max_length=2),
        ),
    ]
