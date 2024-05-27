from django.shortcuts import render
from .models import *

def home(request):
    pagina=request.GET.get('p')
    try:
        pagina=int(pagina)
    except:
        pagina=1
    selezione_inizo=(pagina-1)*24
    selezione_fine=pagina*24
    catalogo=Prodotto.objects.all()[selezione_inizo:selezione_fine]
    paginaMax=int(len(Prodotto.objects.all())/24+1)
    templ = "prodotto/home.html"
    utente = request.user
    ctx = {
        'utente':utente,
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