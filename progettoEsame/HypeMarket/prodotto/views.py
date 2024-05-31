from django.shortcuts import render
from .models import *
from utente.models import *
from HypeMarket.forms import *

def home(request):
    try:
        pagina=int(request.GET.get('p'))
    except:
        pagina=1
    paginaMax=int(len(Prodotto.objects.all())/24+1)
    selezioneInizo=(pagina-1)*24
    selezioneFine=pagina*24
    catalogo=Prodotto.objects.all()[selezioneInizo:selezioneFine]

    templ = 'prodotto/home.html'
    ctx = {
        'title':'Catalogo',
        'catalogo': catalogo, 
        'pagina':pagina,
        'paginaPiu1':pagina+1,
        'paginaPiu2':pagina+2,
        'paginaMeno1':pagina-1,
        'paginaMax':paginaMax
    }
    return render(request,template_name=templ,context=ctx)

def prodotto(request,idModello):
    templ = 'prodotto/prodotto.html'

    for taglia in Taglia.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello)):
        taglia.propostaMinore = None
        taglia.offertaMaggiore = None
        
        if Proposta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').exists():
            proposta = Proposta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').first()
            taglia.propostaMinore = proposta
        if Offerta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').exists():
            offerta = Offerta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').last()
            taglia.offertaMaggiore = offerta

        Taglia.save(taglia)

    prodotto=Prodotto.objects.get(idModello=idModello)
    utente = request.user
    eta=None
    if utente.dataNascita is not None:
        eta=time.now().date().year-utente.dataNascita.year
    ctx = { 
        'eta': eta,
        'prodotto':prodotto,
        'taglie':Taglia.objects.filter(prodotto=prodotto)
    }
    return render(request,template_name=templ,context=ctx)