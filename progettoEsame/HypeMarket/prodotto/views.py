from django.shortcuts import render
from .models import *
from utente.models import *
from HypeMarket.forms import *
from collections import namedtuple

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
    utente=request.user
    wishlist=None
    if utente.is_authenticated:
        wishlist = Wishlist.objects.filter(utente=utente).first().prodotti.all()
    
    ctx = {
        'title':'Catalogo',
        'catalogo': catalogo, 
        'pagina':pagina,
        'paginaPiu1':pagina+1,
        'paginaPiu2':pagina+2,
        'paginaMeno1':pagina-1,
        'paginaMax':paginaMax,
        'wishlist':wishlist
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

    wishlist=None
    if utente.is_authenticated:
        wishlist = Wishlist.objects.filter(utente=utente).first().prodotti.all()

    if utente.is_authenticated:
        if utente.dataNascita is not None:
            eta=time.now().date().year-utente.dataNascita.year

    taglia=checkTaglia(request,prodotto)
    viewOfferte,viewProposte,viewVendite=[],[],[]
    off,prop,vend=False,False,False
    if request.GET.get('taglia') != None: 
        if request.GET.get('viewOfferte') != None:
            off=True
            offerte = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).all()
            for offerta in offerte:
                viewOfferte.append({'data': offerta.data.strftime('%d/%m/%Y'), 'prezzo': offerta.prezzo})
        elif request.GET.get('viewProposte') != None:
            prop=True
            proposte = Proposta.objects.filter(prodotto=prodotto,taglia=taglia).all()
            for proposta in proposte:
                viewProposte.append({'data': proposta.data.strftime('%d/%m/%Y'), 'prezzo': proposta.prezzo})
        elif request.GET.get('viewVendite') != None:
            vend=True
            vendite = Vendita.objects.filter(prodotto=prodotto,taglia=taglia).all()
            for vendita in vendite:
                viewVendite.append({'data': vendita.data.strftime('%d/%m/%Y'), 'prezzo': vendita.prezzo})
    ctx = { 
        'eta': eta,
        'prodotto':prodotto,
        'taglie':Taglia.objects.filter(prodotto=prodotto),
        'viewOfferte':viewOfferte,
        'viewProposte':viewProposte,
        'viewVendite':viewVendite,
        'off':off,
        'prop':prop,
        'vend':vend,
        'wishlist':wishlist
    }
    return render(request,template_name=templ,context=ctx)

def checkTaglia(request,prodotto):
    for t in Taglia.objects.filter(prodotto=prodotto):
        if t.taglia == request.GET.get('taglia'):
            return t
    return None