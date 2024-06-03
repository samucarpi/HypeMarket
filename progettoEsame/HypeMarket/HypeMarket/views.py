from django.shortcuts import render,redirect
from prodotto.models import *
from gestione.models import *
from utente.models import *
from .forms import *
from prodotto.views import paginazione
from utente.views import getWishlist
from django.db.models import Count


def home(request):
    templ = 'home.html'

    topSellers = Vendita.objects.values('prodotto').annotate(nAcquisti=Count('prodotto')).order_by('-nAcquisti')[:8]

    topRated = Recensione.objects.values('prodotto').annotate(nRecensioni=Count('prodotto')).order_by('-nRecensioni')[:8]

    for topSeller in topSellers:
        topSeller['prodotto'] = Prodotto.objects.get(pk=topSeller['prodotto'])

    wishlist = getWishlist(request).prodotti.all()

    ctx ={
        'topSellers':topSellers,
        'form' : Cerca(),
        'wishlist':wishlist,
        'topRated':topRated
    }

    if request.method == 'POST':
        ctx['form'] = Cerca(request.POST)
        form = Cerca(request.POST)
        if form.is_valid() and form.cleaned_data['stringa'] != '':
            stringa = form.cleaned_data['stringa']
            return redirect('/ricerca/'+stringa)
        else:
            return render(request,template_name=templ,context=ctx)
    else:
        form = Cerca()
        return render(request,template_name=templ,context=ctx)

def ricerca(request,stringa):
    templ = 'prodotto/prodotti.html'
    prodotti=Prodotto.objects.filter(titolo__icontains=stringa).all()
    url='/ricerca/'+stringa
    ctx=paginazione(request, prodotti, url, 'Ricerca')

    return render(request,template_name=templ,context=ctx)
