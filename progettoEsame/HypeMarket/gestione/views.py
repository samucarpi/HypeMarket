from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from HypeMarket.forms import *


def checkTaglia(request,prodotto):
    for t in Taglia.objects.filter(prodotto=prodotto):
        if t.taglia == request.GET.get('taglia'):
            return t
    return None


def checkOfferta(form,request):
    if form.cleaned_data['prezzo'] < 0:
        messages.error(request,'Prezzo non valido')
        return False
    return True

@login_required(login_url='utente:Login')
def offerta(request,idModello):
    templ = "utente/modifica.html"
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url='http://localhost:8000/sneakers/'+str(idModello)
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        offertaMaggiore = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last()
        if request.method == 'POST':
            form = OffertaForm(request.POST)
            if form.is_valid() and checkOfferta(form,request):
                if Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
                    Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
                form.save(user=utente,prodotto=prodotto,taglia=taglia)
                return redirect(url)
            else:
                return render(request,template_name=templ,context={'form':form,'url':url,'offerta':True,'offertaMaggiore':offertaMaggiore})
        else:
            form = OffertaForm()
            return render(request,template_name=templ,context={'form':form,'url':url,'offerta':True,'offertaMaggiore':offertaMaggiore})

@login_required(login_url='utente:Login')
def proposta(request,idModello):
    templ = "utente/modifica.html"
    url='http://localhost:8000/sneakers/'+str(idModello)
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        propostaMinore = Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first()
        if request.method == 'POST':
            form = PropostaForm(request.POST)
            if form.is_valid() and checkOfferta(form,request):
                if Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
                    Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
                form.save(user=utente,prodotto=prodotto,taglia=taglia)
                return redirect(url)
            else:
                return render(request,template_name=templ,context={'form':form,'url':url,'proposta':True,'propostaMinore':propostaMinore})
        else:
            form = PropostaForm()
            return render(request,template_name=templ,context={'form':form,'url':url,'proposta':True,'propostaMinore':propostaMinore})

@login_required(login_url='utente:Login')
def vendita(request,idModello):
    templ = "gestione/vendita.html"
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url='http://localhost:8000/sneakers/'+str(idModello)
    taglia=checkTaglia(request,prodotto)
    ctx = {}
    if taglia != None and Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last() and IndirizzoFatturazione.objects.filter(utente=utente).exists() and DatiBancari.objects.filter(utente=utente).exists():
        prezzo = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last().prezzo
        indirizzo = IndirizzoFatturazione.objects.filter(utente=utente).first()
        banca = DatiBancari.objects.filter(utente=utente).first()
        if request.method == 'POST':
            form = VenditaForm(request.POST)
            ctx={
                'form':form,
                'prodotto':prodotto,
                'taglia':taglia,
                'indirizzo':indirizzo,
                'banca':banca,
                'prezzo':prezzo
            }
            if form.is_valid():
                form.save(user=utente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzo=indirizzo,banca=banca)
                Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last().delete()
                taglia.offertaMaggiore
                taglia.save()
                return redirect(url)
            else:
                return render(request,template_name=templ,context=ctx)
        else:
            form = VenditaForm()
            ctx={
                'form':form,
                'prodotto':prodotto,
                'taglia':taglia,
                'indirizzo':indirizzo,
                'banca':banca,
                'prezzo':prezzo
            }
            return render(request,template_name=templ,context=ctx)