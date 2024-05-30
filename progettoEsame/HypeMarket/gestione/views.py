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
    templ = "gestione/vendita.html"
    url='http://localhost:8000/sneakers/'+str(idModello)
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        if Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').exists():
            offertaMaggiore = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last()
            if IndirizzoSpedizione.objects.filter(utente=utente).exists():
                indirizzo = IndirizzoSpedizione.objects.filter(utente=utente).first()
                if CartaCredito.objects.filter(utente=utente).exists():
                    carta = CartaCredito.objects.filter(utente=utente).first()
                    if request.method == 'POST':
                        form = OffertaForm(request.POST)
                        if form.is_valid() and checkOfferta(form,request):
                            if Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
                                Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
                            form.save(user=utente,prodotto=prodotto,taglia=taglia,indirizzo=indirizzo,carta=carta)
                            return redirect(url)
                        else:
                            return render(request,template_name=templ,context={'form':form,'url':url,'offerta':True,'offertaMaggiore':offertaMaggiore})
                    else:
                        form = OffertaForm()
                        return render(request,template_name=templ,context={'form':form,'url':url,'offerta':True,'offertaMaggiore':offertaMaggiore})
                else:
                    messages.error(request,'carta')
                    return redirect(url)
            else:
                messages.error(request,'spedizione')
                return redirect(url)
        else:
            return render(request,template_name=templ,context={'form':form,'url':url,'offerta':True,'offertaMaggiore':None})
    else:
        return redirect(url)

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
    indirizzo,banca,prezzo = None,None,None
    ctx={
        'form':VenditaForm(),
        'prodotto':prodotto,
        'taglia':taglia,
        'indirizzo':indirizzo,
        'banca':banca,
        'prezzo':prezzo,
        'vendita':True
    }

    if Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last() == Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).order_by('prezzo').last():
        messages.error(request, 'errore')
        return redirect(url)

    if taglia != None and Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last() and IndirizzoFatturazione.objects.filter(utente=utente).exists() and DatiBancari.objects.filter(utente=utente).exists():
        prezzo = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last().prezzo
        indirizzo = IndirizzoFatturazione.objects.filter(utente=utente).first()
        banca = DatiBancari.objects.filter(utente=utente).first()
        if request.method == 'POST':
            form = VenditaForm(request.POST)
            if form.is_valid():
                form.save(user=utente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzo=indirizzo,banca=banca)
                offerta = Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last()
                acquirente= offerta.utente
                acquirenteIndirizzo = offerta.IndirizzoSpedizione
                acquirenteCarta= offerta.carta
                data = time.now().date()
                acquisto = Acquisto(utente=acquirente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,IndirizzoSpedizione=acquirenteIndirizzo,carta=acquirenteCarta,data=data)
                Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last().delete()
                acquisto.save()
                return redirect(url)
            else:
                ctx['indirizzo']=indirizzo
                ctx['banca']=banca
                ctx['prezzo']=prezzo
                return render(request,template_name=templ,context=ctx)
        else:
            ctx['indirizzo']=indirizzo
            ctx['banca']=banca
            ctx['prezzo']=prezzo
            return render(request,template_name=templ,context=ctx)
        
@login_required(login_url='utente:Login')
def acquisto(request,idModello):
    templ = "gestione/vendita.html"
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url='http://localhost:8000/sneakers/'+str(idModello)
    taglia=checkTaglia(request,prodotto)
    indirizzo,carta,prezzo = None,None,None
    ctx={
        'form':AcquistoForm(),
        'prodotto':prodotto,
        'taglia':taglia,
        'indirizzo':indirizzo,
        'carta':carta,
        'prezzo':prezzo,
        'vendita':False
    }

    if Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first() == Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).order_by('prezzo').first():
        messages.error(request, 'errore')
        return redirect(url)

    if taglia != None and Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first() and IndirizzoSpedizione.objects.filter(utente=utente).exists() and CartaCredito.objects.filter(utente=utente).exists():
        prezzo = Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first().prezzo
        indirizzo = IndirizzoSpedizione.objects.filter(utente=utente).first()
        carta = CartaCredito.objects.filter(utente=utente).first()
        if request.method == 'POST':
            form = AcquistoForm(request.POST)
            if form.is_valid():
                form.save(user=utente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzo=indirizzo,carta=carta)
                acquirente=Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first().utente
                acquirenteIndirizzo=IndirizzoFatturazione.objects.filter(utente=acquirente).first()
                acquirenteCarta=CartaCredito.objects.filter(utente=acquirente).first()
                acquisto = Acquisto(utente=acquirente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,IndirizzoSpedizione=acquirenteIndirizzo,carta=acquirenteCarta,data=time.now().date())
                acquisto.save()
                Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last().delete()
                return redirect(url)
            else:
                ctx['indirizzo']=indirizzo
                ctx['banca']=carta
                ctx['prezzo']=prezzo
                return render(request,template_name=templ,context=ctx)
        else:
            ctx['indirizzo']=indirizzo
            ctx['banca']=carta
            ctx['prezzo']=prezzo
            return render(request,template_name=templ,context=ctx)