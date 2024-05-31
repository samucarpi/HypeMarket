from django.db import models
from utente.models import Utente,IndirizzoFatturazione,IndirizzoSpedizione,CartaCredito,DatiBancari
from prodotto.models import Prodotto,Taglia

class CompraVendita(models.Model):
    utente=models.ForeignKey(Utente,related_name='mercato', on_delete=models.CASCADE)
    prodotto=models.ForeignKey(Prodotto,related_name='mercato', on_delete=models.CASCADE)
    taglia=models.ForeignKey(Taglia,related_name='mercato', on_delete=models.CASCADE)
    prezzo=models.FloatField()
    data=models.DateField()

class Offerta(CompraVendita):
    indirizzoSpedizione=models.ForeignKey(IndirizzoSpedizione,related_name='offerte', on_delete=models.CASCADE)
    carta=models.ForeignKey(CartaCredito,related_name='offerte', on_delete=models.CASCADE)
    
class Proposta(CompraVendita):
    indirizzoFatturazione=models.ForeignKey(IndirizzoFatturazione,related_name='proposte', on_delete=models.CASCADE)
    banca=models.ForeignKey(DatiBancari,related_name='proposte', on_delete=models.CASCADE)

class Acquisto(CompraVendita):
    indirizzoSpedizione=models.ForeignKey(IndirizzoSpedizione,related_name='acquisti', on_delete=models.CASCADE)
    carta=models.ForeignKey(CartaCredito,related_name='acquisti', on_delete=models.CASCADE)

class Vendita(CompraVendita):
    indirizzoFatturazione=models.ForeignKey(IndirizzoFatturazione,related_name='vendite', on_delete=models.CASCADE)
    banca=models.ForeignKey(DatiBancari,related_name='vendite', on_delete=models.CASCADE)