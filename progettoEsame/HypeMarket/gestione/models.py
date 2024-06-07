from django.db import models
from utente.models import Utente,IndirizzoFatturazione,IndirizzoSpedizione,CartaCredito,DatiBancari
from prodotto.models import Prodotto,Taglia

class CompraVendita(models.Model):
    utente=models.ForeignKey(Utente,related_name='mercato', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='mercato', on_delete=models.PROTECT)
    taglia=models.ForeignKey(Taglia,related_name='mercato', on_delete=models.PROTECT)
    prezzo=models.FloatField()
    data=models.DateField()

class Offerta(CompraVendita):
    indirizzoSpedizione=models.ForeignKey(IndirizzoSpedizione,related_name='offerte', on_delete=models.PROTECT)
    carta=models.ForeignKey(CartaCredito,related_name='offerte', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural='Offerte'
        ordering=['-data']
    
class Proposta(CompraVendita):
    indirizzoFatturazione=models.ForeignKey(IndirizzoFatturazione,related_name='proposte', on_delete=models.PROTECT)
    banca=models.ForeignKey(DatiBancari,related_name='proposte', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural='Proposte'
        ordering=['-data']

class Acquisto(CompraVendita):
    indirizzoSpedizione=models.ForeignKey(IndirizzoSpedizione,related_name='acquisti', on_delete=models.PROTECT)
    carta=models.ForeignKey(CartaCredito,related_name='acquisti', on_delete=models.PROTECT)

    def __str__(self):
        return self.utente.username+' - '+self.prodotto.titolo+' '+self.taglia.taglia+' - '+str(self.prezzo)+'€ - '+str(self.data)

    class Meta:
        verbose_name_plural='Acquisti'
        ordering=['-data']

class Vendita(CompraVendita):
    indirizzoFatturazione=models.ForeignKey(IndirizzoFatturazione,related_name='vendite', on_delete=models.PROTECT)
    banca=models.ForeignKey(DatiBancari,related_name='vendite', on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural='Vendite'
        ordering=['-data']

class Recensione(models.Model):
    acquisto=models.OneToOneField(Acquisto,related_name='recensioni', on_delete=models.CASCADE)
    voto=models.IntegerField()  
    testo=models.TextField()

    class Meta:
        verbose_name_plural='Recensioni'
        ordering=['-acquisto__data']