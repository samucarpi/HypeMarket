# Generated by Django 5.0.6 on 2024-05-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utente', '0002_alter_utente_datanascita_alter_utente_piva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utente',
            name='dataNascita',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='utente',
            name='pIva',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
