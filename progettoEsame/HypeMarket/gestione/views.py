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
    if form.cleaned_data['prezzo'] <= 0:
        messages.error(request,'Prezzo non valido')
        return False
    return True

@login_required(login_url='utente:Login')
def offerta(request,idModello):
    templ = 'gestione/gestione.html'
    url='http://localhost:8000/sneakers/'+str(idModello)
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        if IndirizzoSpedizione.objects.filter(utente=utente).exists():
            indirizzo = IndirizzoSpedizione.objects.filter(utente=utente).first()
            if CartaCredito.objects.filter(utente=utente).exists():
                carta = CartaCredito.objects.filter(utente=utente).first()
                ctx={
                    'form':OffertaForm(),
                    'offerta':True,
                    'taglia':taglia,
                    'prodotto':prodotto,
                    'indirizzo': IndirizzoSpedizione.objects.filter(utente=utente).first(),
                    'carta': CartaCredito.objects.filter(utente=utente).first()
                }
                if request.method == 'POST':
                    form = OffertaForm(request.POST)
                    ctx['form']=form
                    if form.is_valid() and checkOfferta(form,request):
                        if Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
                            Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
                        form.save(utente=utente,prodotto=prodotto,taglia=taglia,indirizzoSpedizione=indirizzo,carta=carta)
                        return redirect(url)
                    else:
                        return render(request,template_name=templ,context=ctx)
                else:
                    return render(request,template_name=templ,context=ctx)
            else:
                messages.error(request,'carta')
                return redirect(url)
        else:
            messages.error(request,'spedizione')
            return redirect(url)
    else:
        return redirect(url)

@login_required(login_url='utente:Login')
def proposta(request,idModello):
    templ = 'gestione/gestione.html'
    url='http://localhost:8000/sneakers/'+str(idModello)
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        if IndirizzoFatturazione.objects.filter(utente=utente).exists():
            indirizzo = IndirizzoFatturazione.objects.filter(utente=utente).first()
            if DatiBancari.objects.filter(utente=utente).exists():
                banca = DatiBancari.objects.filter(utente=utente).first()
                ctx={
                    'form':PropostaForm(),
                    'proposta':True,
                    'taglia':taglia,
                    'prodotto':prodotto,
                    'indirizzo': IndirizzoFatturazione.objects.filter(utente=utente).first(),
                    'banca': DatiBancari.objects.filter(utente=utente).first()
                }
                if request.method == 'POST':
                    form = PropostaForm(request.POST)
                    ctx['form']=form
                    if form.is_valid() and checkOfferta(form,request):
                        if Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
                            Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
                        form.save(utente=utente,prodotto=prodotto,taglia=taglia,indirizzoFatturazione=indirizzo,banca=banca)
                        return redirect(url)
                    else:
                        return render(request,template_name=templ,context=ctx)
                else:
                    return render(request,template_name=templ,context=ctx)
            else:
                messages.error(request,'banca')
                return redirect(url)
        else:
            messages.error(request,'fatturazione')
            return redirect(url)
    else:
        return redirect(url)

@login_required(login_url='utente:Login')
def vendita(request,idModello):
    templ = 'gestione/gestione.html'
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url='http://localhost:8000/sneakers/'+str(idModello)
    taglia=checkTaglia(request,prodotto)

    if Offerta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').last() == Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).order_by('prezzo').last():
        messages.error(request, 'corrispondenteVendita')
        return redirect(url)

    if taglia != None:
        if IndirizzoFatturazione.objects.filter(utente=utente).exists():
            indirizzoFatturazione = IndirizzoFatturazione.objects.filter(utente=utente).first()
            if DatiBancari.objects.filter(utente=utente).exists():
                banca = DatiBancari.objects.filter(utente=utente).first()
                ctx={
                    'form':VenditaForm(),
                    'prodotto':prodotto,
                    'taglia':taglia,
                    'indirizzo':indirizzoFatturazione,
                    'banca':banca,
                    'vendita':True
                }
                if request.method == 'POST':
                    form = VenditaForm(request.POST)
                    ctx['form']=form
                    if form.is_valid():
                        offertaRiferimento= taglia.offertaMaggiore
                        prezzo = offertaRiferimento.prezzo
                        form.save(utente=utente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzoFatturazione=indirizzoFatturazione,banca=banca)
                        acquirente = offertaRiferimento.utente
                        indirizzoSpedizione = offertaRiferimento.indirizzoSpedizione
                        carta = offertaRiferimento.carta
                        data = time.now().date()
                        acquisto = Acquisto(utente=acquirente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzoSpedizione=indirizzoSpedizione,carta=carta,data=data)
                        offertaRiferimento.delete()
                        acquisto.save()
                        return redirect(url)
                    else:
                        return render(request,template_name=templ,context=ctx)
                else:
                    return render(request,template_name=templ,context=ctx)
            else:
                messages.error(request,'banca')
                return redirect(url)
        else:
            messages.error(request,'fatturazione')
            return redirect(url)
    else:
        return redirect(url)
        
@login_required(login_url='utente:Login')
def acquisto(request,idModello):
    templ = 'gestione/gestione.html'
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url='http://localhost:8000/sneakers/'+str(idModello)
    taglia=checkTaglia(request,prodotto)

    if Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first() == Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).order_by('prezzo').first():
        messages.error(request, 'corrispondenteAcquisto')
        return redirect(url)

    if taglia != None:
        if IndirizzoSpedizione.objects.filter(utente=utente).exists():
            indirizzo = IndirizzoSpedizione.objects.filter(utente=utente).first()
            if CartaCredito.objects.filter(utente=utente).exists():
                carta = CartaCredito.objects.filter(utente=utente).first()
                ctx={
                    'form':AcquistoForm(),
                    'prodotto':prodotto,
                    'taglia':taglia,
                    'indirizzo':indirizzo,
                    'carta':carta,
                    'acquisto':True
                }
                if request.method == 'POST':
                    form = AcquistoForm(request.POST)
                    ctx['form']=form
                    if form.is_valid():
                        propostaRiferimento= taglia.propostaMinore
                        prezzo = propostaRiferimento.prezzo
                        form.save(utente=utente,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzoSpedizione=indirizzo,carta=carta)
                        venditore = propostaRiferimento.utente
                        indirizzoFatturazione = propostaRiferimento.indirizzoFatturazione
                        banca = propostaRiferimento.banca
                        data = time.now().date()
                        acquisto = Vendita(utente=venditore,prodotto=prodotto,taglia=taglia,prezzo=prezzo,indirizzoFatturazione=indirizzoFatturazione,banca=banca,data=data)
                        Proposta.objects.filter(prodotto=prodotto,taglia=taglia).order_by('prezzo').first().delete()
                        acquisto.save()
                        return redirect(url)
                    else:
                        return render(request,template_name=templ,context=ctx)
                else:
                    return render(request,template_name=templ,context=ctx)
            else:
                messages.error(request,'carta')
                return redirect(url)
        else:
            messages.error(request,'spedizione')
            return redirect(url)
    else:
        return redirect(url)

@login_required(login_url='utente:Login')
def eliminaProposta(request,idModello):
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url=request.META.get('HTTP_REFERER', '/').split('?')[0]
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        if Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
            Proposta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
        return redirect(url)
    else:
        return redirect(url)

@login_required(login_url='utente:Login')
def eliminaOfferta(request,idModello):
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url=request.META.get('HTTP_REFERER', '/').split('?')[0]
    taglia=checkTaglia(request,prodotto)
    if taglia != None:
        if Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).exists():
            Offerta.objects.filter(utente=utente,prodotto=prodotto,taglia=taglia).delete()
        return redirect(url)
    else:
        return redirect(url)