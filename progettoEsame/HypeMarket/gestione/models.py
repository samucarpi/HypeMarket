from django.db import models
from utente.models import *
from prodotto.models import *

class Offerta(models.Model):
    utente=models.ForeignKey(Utente,related_name='offerte', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='offerte', on_delete=models.CASCADE)
    taglia=models.ForeignKey(Taglia,related_name='offerte', on_delete=models.CASCADE)
    prezzo=models.FloatField()
    data=models.DateField()

class Proposta(models.Model):
    utente=models.ForeignKey(Utente,related_name='proposte', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='proposte', on_delete=models.CASCADE)
    taglia=models.ForeignKey(Taglia,related_name='proposte', on_delete=models.CASCADE)
    prezzo=models.FloatField()
    data=models.DateField()

class Acquisto(models.Model):
    utente=models.ForeignKey(Utente,related_name='acquisti', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='acquisti', on_delete=models.CASCADE)
    taglia=models.ForeignKey(Taglia,related_name='acquisti', on_delete=models.CASCADE)
    prezzo=models.FloatField()
    data=models.DateField()

class Vendita(models.Model):
    utente=models.ForeignKey(Utente,related_name='vendite', on_delete=models.CASCADE)
    indirizzoFatturazione=models.ForeignKey(IndirizzoFatturazione,related_name='vendite', on_delete=models.CASCADE)
    banca=models.ForeignKey(DatiBancari,related_name='vendite', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='vendite', on_delete=models.CASCADE)
    taglia=models.ForeignKey(Taglia,related_name='vendite', on_delete=models.CASCADE)
    prezzo=models.FloatField()
    data=models.DateField()
