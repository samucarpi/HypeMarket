from django.db import models
from prodotto.models import Prodotto
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from datetime import datetime as time

class Utente(AbstractUser):
    username=models.CharField(max_length=25,unique=True)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    email=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    dataNascita=models.DateField(null=True, blank=True)
    pIva=models.CharField(max_length=11,null=True, blank=True)

    class Meta: 
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

class Indirizzo(models.Model):
    utente=models.ForeignKey(Utente,related_name='indirizzi', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25,default='Uknown')
    cognome=models.CharField(max_length=25,default='Uknown')
    via=models.CharField(max_length=50,default='Uknown')
    citta=models.CharField(max_length=50,default='Uknown')
    cap=models.CharField(max_length=5,default='Uknown')
    provincia=models.CharField(max_length=2,default='Uknown')
    nazione=CountryField()
    telefono=models.CharField(max_length=15,default='Uknown')

class IndirizzoSpedizione(Indirizzo):
    pass

class IndirizzoFatturazione(Indirizzo):
    pass

class DatiBancari(models.Model):
    utente=models.ForeignKey(Utente,related_name='dati', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25,default='Uknown')
    cognome=models.CharField(max_length=25,default='Uknown')
    iban=models.CharField(max_length=27,default='Uknown')
    banca=models.CharField(max_length=50,default='Uknown')

class CartaCredito(models.Model):
    utente=models.ForeignKey(Utente,related_name='carte', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25,default='Uknown')
    cognome=models.CharField(max_length=25,default='Uknown')
    numero=models.CharField(max_length=16,default='Uknown')
    scadenzaMese=models.CharField(max_length=2)
    scadenzaAnno=models.CharField(max_length=4)
    cvv=models.CharField(max_length=3,default='Uknown')

class Wishlist(models.Model):
    utente=models.ForeignKey(Utente,related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Prodotto)

class Offerta(models.Model):
    utente=models.ForeignKey(Utente,related_name='offerte', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='offerte', on_delete=models.CASCADE)
    prezzo=models.FloatField()
    data=models.DateField()