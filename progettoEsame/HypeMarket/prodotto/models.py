from django.db import models

class Prodotto(models.Model):
    titolo=models.CharField(max_length=50)
    immagine=models.CharField(max_length=200)
    idModello=models.CharField(max_length=10)
    dataRilascio=models.DateField()

    def __str__(self):
        return self.titolo
    
    class Meta:
        verbose_name_plural='Prodotti'
        ordering=['-dataRilascio']

class Taglia(models.Model):
    prodotto=models.ForeignKey(Prodotto,related_name='taglie', on_delete=models.CASCADE)
    taglia=models.CharField(max_length=5)
    propostaMinore=models.OneToOneField('gestione.Proposta',related_name='taglie', on_delete=models.SET_NULL,blank=True,null=True)
    offertaMaggiore=models.OneToOneField('gestione.Offerta',related_name='taglie', on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.taglia

    class Meta:
        verbose_name_plural='Taglie'

    