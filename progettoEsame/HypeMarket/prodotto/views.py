from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from utente.models import *
from HypeMarket.forms import *

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

    for taglia in Taglia.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello)):
        if Proposta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').first():
            proposta = Proposta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').first()
            taglia.propostaMinore = proposta.prezzo
            Taglia.save(taglia)
        if Offerta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').last():
            offerta = Offerta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').last().prezzo
            taglia.offertaMaggiore = offerta
            Taglia.save(taglia)
    
    ctx = { 
        "prodotto":Prodotto.objects.get(idModello=idModello),
        "taglie":Taglia.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello))
    }
    return render(request,template_name=templ,context=ctx)