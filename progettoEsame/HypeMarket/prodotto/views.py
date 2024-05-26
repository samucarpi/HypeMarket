from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def catalogo(request):
    for k in request.GET:
        pagina=request.GET[k]
    pagina=int(pagina)
    selezione_inizo=(pagina-1)*24
    selezione_fine=pagina*24
    catalogo=Prodotto.objects.all()[selezione_inizo:selezione_fine]
    paginaMax=int(len(Prodotto.objects.all())/24+1)
    templ = "prodotto/catalogo.html"
    ctx = { 
        "title":"Catalogo sneakers", 
        "catalogo": catalogo, 
        "taglie":Taglia.objects.all(),
        'pagina':pagina,
        'paginaPiu1':pagina+1,
        'paginaPiu2':pagina+2,
        'paginaMeno1':pagina-1,
        'paginaMax':paginaMax
    }
    return render(request,template_name=templ,context=ctx)

def prodotto(request,idModello):
    templ = "prodotto/prodotto.html"
    ctx = { 
        "titolo":Prodotto.objects.get(idModello=idModello).titolo,
        "immagine":Prodotto.objects.get(idModello=idModello).immagine,
        "idModello":Prodotto.objects.get(idModello=idModello).idModello,
        "dataRilascio":Prodotto.objects.get(idModello=idModello).dataRilascio,
        "taglie":Taglia.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello))
    }
    return render(request,template_name=templ,context=ctx)