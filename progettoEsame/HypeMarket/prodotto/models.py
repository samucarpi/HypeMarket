from django.db import models
from datetime import datetime

class Prodotto(models.Model):
    titolo=models.CharField(max_length=50)
    immagine=models.CharField(max_length=200)
    idModello=models.CharField(max_length=10)
    dataRilascio=models.DateField()

    def __str__(self):
        out = self.titolo + " \n " + self.immagine + " \n " + self.idModello + " \n " + self.dataRilascio.strftime("%d %M %Y") + " \n "
        return out

class Taglia(models.Model):
    prodotto=models.ForeignKey(Prodotto,related_name='taglie', on_delete=models.CASCADE)
    taglia=models.CharField(max_length=5)

    def __str__(self):
        out = self.taglia + " \n "
        return out