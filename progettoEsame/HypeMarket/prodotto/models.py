from django.db import models

class Prodotto(models.Model):
    titolo=models.CharField(max_length=50)
    immagine=models.CharField(max_length=200)
    idModello=models.CharField(max_length=10)
    dataRilascio=models.DateField()

class Taglia(models.Model):
    prodotto=models.ForeignKey(Prodotto,related_name='taglie', on_delete=models.CASCADE)
    taglia=models.CharField(max_length=5)
    propostaMinore=models.ForeignKey('gestione.Proposta',related_name='taglie', on_delete=models.SET_NULL,blank=True,null=True)
    offertaMaggiore=models.ForeignKey('gestione.Offerta',related_name='taglie', on_delete=models.SET_NULL,blank=True,null=True)