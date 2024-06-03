from django.shortcuts import render,redirect
from prodotto.models import *
from utente.models import *
from .forms import *
from prodotto.views import paginazione

def home(request):
    templ = 'home.html'
    if request.method == 'POST':
        form = Cerca(request.POST)
        if form.is_valid() and form.cleaned_data['stringa'] != '':
            stringa = form.cleaned_data['stringa']
            return redirect('/ricerca/'+stringa)
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Cerca()
        return render(request,template_name=templ,context={'form':form})

def ricerca(request,stringa):
    templ = 'prodotto/prodotti.html'
    prodotti=Prodotto.objects.filter(titolo__icontains=stringa).all()
    url='/ricerca/'+stringa
    ctx=paginazione(request, prodotti, url, 'Ricerca')

    return render(request,template_name=templ,context=ctx)