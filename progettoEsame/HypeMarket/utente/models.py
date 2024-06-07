from django.db import models
from prodotto.models import *
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

class Utente(AbstractUser):
    username=models.CharField(max_length=25,unique=True)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    email=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    dataNascita=models.DateField(null=True, blank=True)
    immagineProfilo=models.FileField(blank=True, null=True)
    pIva=models.CharField(max_length=11,null=True, blank=True)

@receiver(pre_save, sender=Utente)
def setAdminInfo(sender, instance, **kwargs):
    if instance.is_superuser and not instance.pk:
        if not instance.nome:
            instance.nome = "admin"
        if not instance.cognome:
            instance.cognome = "admin"

@receiver(post_save, sender=Utente)
def setWishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(utente=instance)

class Indirizzo(models.Model):
    utente=models.ForeignKey(Utente,related_name='indirizzi', on_delete=models.CASCADE,null=True, blank=True)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    via=models.CharField(max_length=50)
    citta=models.CharField(max_length=50)
    cap=models.CharField(max_length=5)
    provincia=models.CharField(max_length=2)
    nazione=CountryField()
    telefono=models.CharField(max_length=15)

    def __str__(self):
        return self.nome+' '+self.cognome+' - '+self.via+', '+self.citta+', '+self.cap+', '+self.provincia+', '+str(self.nazione)+' - '+self.telefono

class IndirizzoSpedizione(Indirizzo):
    pass

    class Meta:
        verbose_name_plural='Indirizzi di spedizione'

class IndirizzoFatturazione(Indirizzo):
    pass

    class Meta:
        verbose_name_plural='Indirizzi di fatturazione'

class DatiBancari(models.Model):
    utente=models.OneToOneField(Utente,related_name='dati', on_delete=models.CASCADE,null=True, blank=True)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    iban=models.CharField(max_length=27)
    banca=models.CharField(max_length=50)

    def __str__(self):
        return self.nome+' '+self.cognome+' - '+self.iban+' - '+self.banca

    class Meta:
        verbose_name_plural='Dati bancari'

class CartaCredito(models.Model):
    utente=models.OneToOneField(Utente,related_name='carte', on_delete=models.CASCADE,null=True, blank=True)
    nome=models.CharField(max_length=25)
    cognome=models.CharField(max_length=25)
    numero=models.CharField(max_length=16)
    scadenzaMese=models.CharField(max_length=2)
    scadenzaAnno=models.CharField(max_length=4)
    cvv=models.CharField(max_length=3)

    def __str__(self):
        return self.nome+' '+self.cognome+' - '+self.numero+' - '+self.scadenzaMese+'/'+self.scadenzaAnno+' - '+self.cvv

    class Meta:
        verbose_name_plural='Carte di credito'

class Wishlist(models.Model):
    utente=models.OneToOneField(Utente,related_name='wishlist', on_delete=models.CASCADE,null=True, blank=True)
    prodotti = models.ManyToManyField(Prodotto)