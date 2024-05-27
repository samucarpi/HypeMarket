from django.db import models
from prodotto.models import Prodotto
from django.contrib.auth.models import AbstractUser

class Utente(AbstractUser):
    class Meta: 
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

    nome=models.CharField(max_length=25,default='')
    cognome=models.CharField(max_length=25,default='')
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    dataNascita=models.DateField(null=True,blank=True)
    pIva=models.CharField(max_length=11,blank=True,null=True)

class Indirizzo(models.Model):
    utente=models.ForeignKey(Utente,related_name='indirizzi', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25,default='')
    cognome=models.CharField(max_length=25,default='')
    via=models.CharField(max_length=50)
    citta=models.CharField(max_length=50)
    cap=models.CharField(max_length=5)
    provincia=models.CharField(max_length=2)
    nazione=models.CharField(max_length=50)
    telefono=models.CharField(max_length=15)

class IndirizzoSpedizione(Indirizzo):
    pass

class IndirizzoFatturazione(Indirizzo):
    pass

class DatiBancari(models.Model):
    utente=models.ForeignKey(Utente,related_name='dati', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25,default='')
    cognome=models.CharField(max_length=25,default='')
    iban=models.CharField(max_length=27)
    banca=models.CharField(max_length=50)

class CartaCredito(models.Model):
    utente=models.ForeignKey(Utente,related_name='carte', on_delete=models.CASCADE)
    nome=models.CharField(max_length=25,default='')
    cognome=models.CharField(max_length=25,default='')
    numero=models.CharField(max_length=16)
    scadenza=models.DateField()
    cvv=models.CharField(max_length=3)

class Wishlist(models.Model):
    utente=models.ForeignKey(Utente,related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Prodotto)
