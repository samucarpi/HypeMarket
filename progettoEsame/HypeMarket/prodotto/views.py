from django.shortcuts import render
from .models import *
from utente.models import *
from HypeMarket.forms import *
from django.db.models import Avg

def getWishlist(request):
    utente = request.user
    wishlist = None
    if utente.is_authenticated:
        wishlist = Wishlist.objects.filter(utente=utente).first()
    return wishlist

def paginazione(request, prodotti, url):
    paginaMax = int(len(prodotti)/24+1)
    try:
        pagina = int(request.GET.get('p'))
    except:
        pagina = 1
    if pagina > paginaMax:
        pagina=paginaMax
    selezioneInizo = (pagina-1)*24
    selezioneFine = pagina*24

    try:
        wishlist=getWishlist(request).prodotti.all()
    except:
        wishlist=None
    
    ctx = {
        'prodotti': prodotti[selezioneInizo:selezioneFine], 
        'pagina': pagina,
        'paginaPiu1': pagina + 1,
        'paginaPiu2': pagina + 2,
        'paginaMeno1': pagina - 1,
        'paginaMax': paginaMax,
        'url': url,
        'wishlist': wishlist
    }

    return ctx


def catalogo(request):
    templ = 'prodotto/prodotti.html'

    wishlist = getWishlist(request)
    try:
        wishlistProd = wishlist.prodotti.all()
        wishlistOut = Prodotto.objects.exclude(id__in=wishlistProd.values('id'))
        prodotti = list(wishlistProd)+list(wishlistOut)
    except:
        prodotti = Prodotto.objects.all()
        wishlist = None
    
    url = '/sneakers/catalogo'

    ctx = paginazione(request, prodotti, url)

    return render(request,template_name=templ,context=ctx)

def checkTaglia(request,prodotto):
    for t in Taglia.objects.filter(prodotto=prodotto):
        if t.taglia == request.GET.get('taglia'):
            return t
    return None

def aggiornaPrezzi(prodotto,taglia):
    for taglia in Taglia.objects.filter(prodotto=prodotto):
        taglia.propostaMinore = None
        taglia.offertaMaggiore = None
        if Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').exists():
            proposta = Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first()
            taglia.propostaMinore = proposta
        if Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').exists():
            offerta = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last()
            taglia.offertaMaggiore = offerta
        taglia.save()

def prodotto(request,idModello):
    templ = 'prodotto/prodotto.html'

    prodotto=Prodotto.objects.get(idModello=idModello)

    utente = request.user
    eta=None

    wishlist=getWishlist(request).prodotti.all()
    
    if utente.is_authenticated:
        if utente.dataNascita is not None:
            eta=time.now().date().year-utente.dataNascita.year

    taglia=checkTaglia(request,prodotto)
    aggiornaPrezzi(prodotto,taglia)

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

    recensioni = Recensione.objects.filter(acquisto__prodotto=prodotto).all()
    mediaRecensioni = Recensione.objects.filter(acquisto__prodotto=prodotto).aggregate(Avg('voto'))['voto__avg']
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
        'wishlist':wishlist,
        'recensioni':recensioni,
        'mediaRecensioni':mediaRecensioni,
    }
    return render(request,template_name=templ,context=ctx)