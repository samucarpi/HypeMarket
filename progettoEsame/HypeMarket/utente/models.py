from django.db import models
from prodotto.models import Prodotto

class Utente(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    nome=models.CharField(max_length=50)
    cognome=models.CharField(max_length=50)
    dataNascita=models.DateField(null=True,blank=True)
    pIva=models.CharField(max_length=11,blank=True,null=True)

class Indirizzo(models.Model):
    utente=models.ForeignKey(Utente,related_name='indirizzi', on_delete=models.CASCADE)
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

class CartaCredito(models.Model):
    utente=models.ForeignKey(Utente,related_name='carte', on_delete=models.CASCADE)
    numero=models.CharField(max_length=16)
    scadenza=models.DateField()
    cvv=models.CharField(max_length=3)

class Wishlist(models.Model):
    utente=models.ForeignKey(Utente,related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(Prodotto)

class createUser(models.Model):
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    nome=models.CharField(max_length=50)
    cognome=models.CharField(max_length=50)
    dataNascita=models.DateField()
    pIva=models.CharField(max_length=11)
    via=models.CharField(max_length=50)
    citta=models.CharField(max_length=50)
    cap=models.CharField(max_length=5)
    provincia=models.CharField(max_length=2)
    nazione=models.CharField(max_length=50)
    titolo=models.CharField(max_length=50)
    numero=models.CharField(max_length=16)
    scadenza=models.DateField()
    cvv=models.CharField(max_length=3)
    products = models.ManyToManyField(Prodotto)