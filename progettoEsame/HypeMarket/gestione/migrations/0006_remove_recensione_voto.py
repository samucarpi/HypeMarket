# Generated by Django 5.0.6 on 2024-06-04 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestione', '0005_alter_recensione_voto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recensione',
            name='voto',
        ),
    ]