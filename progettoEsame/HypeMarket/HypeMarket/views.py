from django.shortcuts import render,redirect
from prodotto.models import *
from gestione.models import *
from utente.models import *
from .forms import *
from prodotto.views import paginazione
from utente.views import getWishlist
from django.db.models import Count,Avg
import urllib.parse

def home(request):
    templ = 'home.html'

    topSellers = Acquisto.objects.values('prodotto').annotate(nAcquisti=Count('prodotto')).order_by('-nAcquisti')[:8]
    topRated = Recensione.objects.values('acquisto__prodotto').annotate(media=Avg('voto')).order_by('-media')[:8]
    topVenduti,topVotati = [],[]
    for topSeller in topSellers:
        topVenduti.append({'prodotto':Prodotto.objects.get(pk=topSeller['prodotto']),'nAcquisti':topSeller['nAcquisti']})
    for topRate in topRated:
        topVotati.append({'prodotto':Prodotto.objects.get(pk=topRate['acquisto__prodotto']),'media':topRate['media']})

    try:
        wishlist=getWishlist(request).prodotti.all()
    except:
        wishlist=None

    form = Cerca()

    ctx ={
        'form' : form,
        'wishlist':wishlist,
        'topVenduti':topVenduti,
        'topVotati':topVotati
    }

    if request.method == 'POST':
        form = Cerca(request.POST)
        ctx['form'] = form
        if form.is_valid() and form.cleaned_data['stringa'] != '':
            stringa = form.cleaned_data['stringa']
            return redirect('/ricerca/'+stringa)
        else:
            return render(request,template_name=templ,context=ctx)
    else:
        return render(request,template_name=templ,context=ctx)

def ricerca(request,stringa):
    templ = 'prodotto/prodotti.html'
    prodotti=Prodotto.objects.filter(titolo__icontains=stringa).all()
    url='/ricerca/'+stringa
    ctx=paginazione(request, prodotti, url, 'Ricerca')
    ctx['ricerca']=urllib.parse.unquote(stringa)

    return render(request,template_name=templ,context=ctx)
