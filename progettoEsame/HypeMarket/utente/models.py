from django.db import models
from prodotto.models import *
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

class Utente(AbstractUser):
    username=models.CharField(max_length=25,unique=True)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    email=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    dataNascita=models.DateField(null=True, blank=True)
    pIva=models.CharField(max_length=11,null=True, blank=True)

    class Meta: 
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

class Indirizzo(models.Model):
    utente=models.ForeignKey(Utente,related_name='indirizzi', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    via=models.CharField(max_length=50)
    citta=models.CharField(max_length=50)
    cap=models.CharField(max_length=5)
    provincia=models.CharField(max_length=2)
    nazione=CountryField()
    telefono=models.CharField(max_length=15)

class IndirizzoSpedizione(Indirizzo):
    pass

class IndirizzoFatturazione(Indirizzo):
    pass

class DatiBancari(models.Model):
    utente=models.ForeignKey(Utente,related_name='dati', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    iban=models.CharField(max_length=27)
    banca=models.CharField(max_length=50)

class CartaCredito(models.Model):
    utente=models.ForeignKey(Utente,related_name='carte', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    numero=models.CharField(max_length=16)
    scadenzaMese=models.CharField(max_length=2)
    scadenzaAnno=models.CharField(max_length=4)
    cvv=models.CharField(max_length=3)

class Wishlist(models.Model):
    utente=models.ForeignKey(Utente,related_name='wishlist', on_delete=models.CASCADE)
    prodotti = models.ManyToManyField(Prodotto)

class Recensione(models.Model):
    utente=models.ForeignKey(Utente,related_name='recensioni', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='recensioni', on_delete=models.CASCADE)
    testo=models.TextField()
    voto=models.IntegerField()