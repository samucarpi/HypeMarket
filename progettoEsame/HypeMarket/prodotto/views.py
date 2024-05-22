from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def catalogo(request):
    templ = "prodotto/catalogo.html"
    ctx = { "title":"Catalogo sneakers", "catalogo": Prodotto.objects.all(), "taglie":Taglia.objects.all(),'tot':range(1,10)}
    return render(request,template_name=templ,context=ctx)