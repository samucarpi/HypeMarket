from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from HypeMarket.forms import *
from datetime import datetime as time

def checkPassword(form,request):
    if form.cleaned_data['password'] != form.cleaned_data['confermaPassword']:
        messages.error(request,'Password non corrispondenti')
        return False
    return True

def registrazioneForm(request):
    templ='utente/registrazioneLogin.html'
    if request.method == 'POST':
        form = Registrazione(request.POST)
        if form.is_valid() and checkPassword(form,request):
            form.save()
            wishlist = Wishlist()
            wishlist.utente = Utente.objects.get(username=form.cleaned_data['username'])
            wishlist.save()
            messages.success(request, 'Sei stato registrato con successo!')
            return redirect('utente:Login')
        else:
            return render(request,template_name=templ,context={'form':form,'login':False})
    else:
        form = Registrazione()
        return render(request,template_name=templ,context={'form':form,'login':False})

def checkLogin(form,request):
    utente = authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
    if utente is None:
        return None
    return utente

def loginForm(request):
    templ='utente/registrazioneLogin.html'
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            utente = checkLogin(form,request)
            if utente:
                login(request,utente)
                return redirect('utente:Account')
            else:
                messages.error(request,'Email o password errati')
                return redirect('utente:Account')
        else:
            messages.error(request,'Email o password errati')
            return render(request,template_name=templ,context={'form':form,'login':True})
    else:
        form = Login()
        return render(request,template_name=templ,context={'form':form,'login':True})
    
def logoutAction(request):
    logout(request)
    return redirect('/sneakers/catalogo')
    
@login_required(login_url='utente:Login')
def account(request):
    templ='utente/account.html'
    utente = request.user
    indirizzoSpedizione,indirizzoFatturazione,banca,carta=None,None,None,None
    if IndirizzoSpedizione.objects.filter(utente=utente).exists():
        indirizzoSpedizione=IndirizzoSpedizione.objects.filter(utente=utente).first()
    if IndirizzoFatturazione.objects.filter(utente=utente).exists():
        indirizzoFatturazione=IndirizzoFatturazione.objects.filter(utente=utente).first()
    if DatiBancari.objects.filter(utente=utente).exists():
        banca= DatiBancari.objects.filter(utente=utente).first()
    if CartaCredito.objects.filter(utente=utente).exists():
        carta=CartaCredito.objects.filter(utente=utente).first()
    ctx = {
        'utente':utente,
        'indirizzoSpedizione':indirizzoSpedizione,
        'indirizzoFatturazione':indirizzoFatturazione,
        'banca':banca,
        'carta':carta
    }
    return render(request,template_name=templ,context=ctx)

def checkData(form,request):
    data = form.cleaned_data['dataNascita']
    if data is not None:
        if  data > time.now().date():
            messages.error(request,'Data di nascita non valida')
            return False
        if data.year < 1900:
            messages.error(request,'Data di nascita non valida')
            return False
        if time.now().year - data.year > 100:
            messages.error(request,'Data di nascita non valida')
            return False
        if time.now().year - data.year < 18:
            messages.error(request,'È necessario avere almeno 18 anni')
            return False
        return True
    else:
        return True
    
def eliminaDatiEsistenti(tipo,utente):
    if tipo.objects.filter(utente=utente).exists():
        try:
            tipo.objects.filter(utente=utente).first().delete()
        except:
            tipo.objects.filter(utente=utente).update(utente=None)

def checkBanca(form,request):
    if len(form.cleaned_data['iban']) != 27:
        messages.error(request,'IBAN non valido')
        return False
    return True
    
def checkCarta(form,request):
    try:
        int(form.cleaned_data['numero'])
        scadenzaMese=int(form.cleaned_data['scadenzaMese'])
        scadenzaAnno=int(form.cleaned_data['scadenzaAnno'])
        int(form.cleaned_data['cvv'])
    except ValueError:
        messages.error(request,'Inserire solo numeri')
        return False
    if len(form.cleaned_data['numero']) != 16:
        messages.error(request,'Numero carta non valido')
        return False
    if len(form.cleaned_data['scadenzaMese']) != 2 or (scadenzaMese < 1 or scadenzaMese > 12):
        messages.error(request,'Mese scadenza non valido')
        return False
    if len(form.cleaned_data['scadenzaAnno']) != 4 or (scadenzaAnno < time.now().year or scadenzaAnno > time.now().year+10):
        messages.error(request,'Anno scadenza non valido')
        return False
    if scadenzaMese<time.now().month and scadenzaAnno==time.now().year:
        messages.error(request,'Mese scadenza non valido')
        return False
    if len(form.cleaned_data['cvv']) != 3:
        messages.error(request,'CVV non valido')
        return False
    return True

@login_required(login_url='utente:Login')
def modifica(request,tipo):
    templ = 'utente/modifica.html'
    utente = request.user
    if tipo == 'informazioni':
        form = Informazioni()
    elif tipo == 'indirizzo-spedizione':
        form = Spedizione()
    elif tipo == 'indirizzo-fatturazione':
        form = Fatturazione()
    elif tipo == 'banca':
        form = Banca()
    elif tipo == 'carta':
        form = Carta()
    if request.method == 'POST':
        if tipo == 'informazioni':
            form = Informazioni(request.POST)
        elif tipo == 'indirizzo-spedizione':
            form = Spedizione(request.POST)
        elif tipo == 'indirizzo-fatturazione':
            form = Fatturazione(request.POST)
        elif tipo == 'banca':
            form = Banca(request.POST)
        elif tipo == 'carta':
            form = Carta(request.POST)
        if form.is_valid():
            if tipo=='informazioni' and checkData(form,request):
                form.save(utente=utente)
                return redirect('utente:Account')
            elif tipo == 'indirizzo-spedizione':
                eliminaDatiEsistenti(IndirizzoSpedizione,utente)
                form.save(utente=utente)
                return redirect('utente:Account')
            elif tipo == 'indirizzo-fatturazione': 
                eliminaDatiEsistenti(IndirizzoFatturazione,utente)
                form.save(utente=utente)
                return redirect('utente:Account')
            elif tipo == 'banca' and checkBanca(form,request):
                eliminaDatiEsistenti(DatiBancari,utente)
                form.save(utente=utente)
                return redirect('utente:Account')
            elif tipo == 'carta' and checkCarta(form,request):
                eliminaDatiEsistenti(CartaCredito,utente)
                form.save(utente=utente)
                return redirect('utente:Account')
            else:
                return render(request,template_name=templ,context={'form':form})
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        return render(request,template_name=templ,context={'form':form})

@login_required(login_url='utente:Login')
def elimina(request,tipo):
    utente = request.user
    if tipo == 'informazioni':
        if utente.dataNascita is not None:
            utente.dataNascita = None
        if utente.pIva is not None:
            utente.pIva = None
        utente.save()
        
    if tipo == 'indirizzo-spedizione':
        eliminaDatiEsistenti(IndirizzoSpedizione,utente)
    elif tipo == 'indirizzo-fatturazione':
        eliminaDatiEsistenti(IndirizzoFatturazione,utente)
    elif tipo == 'banca':
        eliminaDatiEsistenti(DatiBancari,utente)
    elif tipo == 'carta':
        eliminaDatiEsistenti(CartaCredito,utente)
    elif tipo == 'account':
        utente.delete()
        return redirect('utente:Login')
    return redirect('utente:Account')

def getWishlist(request):
    utente = request.user
    wishlist = None
    if utente.is_authenticated:
        wishlist = Wishlist.objects.filter(utente=utente).first()
    return wishlist

@login_required(login_url='utente:Login')
def aggiungiPreferiti(request,idModello):
    url=request.META.get('HTTP_REFERER', '/').split('?')[0]
    if request.GET.get('p'):
        try:
            pagina=int(request.GET.get('p'))
        except:
            pagina=1
        url=url +'?p='+str(pagina)
    
    prodotto=Prodotto.objects.filter(idModello=idModello).first()
    wishlist = getWishlist(request)
    if prodotto not in wishlist.prodotti.all():
        wishlist.prodotti.add(prodotto)
        wishlist.save()
    else:
        wishlist.prodotti.remove(prodotto)
        wishlist.save()
    return redirect(url,idModello=idModello)

@login_required(login_url='utente:Login')
def wishlist(request):
    templ = 'utente/wishlist.html'
    wishlist = getWishlist(request)
    try:
        pagina=int(request.GET.get('p'))
    except:
        pagina=1
    paginaMax=int(len(wishlist.prodotti.all())/24+1)
    selezioneInizo=(pagina-1)*24
    selezioneFine=pagina*24
    wishlist=wishlist.prodotti.all()[selezioneInizo:selezioneFine]
    
    ctx = {
        'title':'Wishlist',
        'pagina':pagina,
        'paginaPiu1':pagina+1,
        'paginaPiu2':pagina+2,
        'paginaMeno1':pagina-1,
        'paginaMax':paginaMax,
        'wishlist':wishlist,
        'url':'/utente/wishlist'
    }

    return render(request,template_name=templ,context=ctx)

@login_required(login_url='utente:Login')
def vendite(request):
    templ = 'utente/venditeAcquisti.html'
    utente = request.user
    vendite = Vendita.objects.filter(utente=utente).all().order_by('data')
    proposte = Proposta.objects.filter(utente=utente).all().order_by('data')
    ctx = {
        'title':'Vendite e proposte',
        'vendite': vendite,
        'proposte' : proposte,
        'viewVendite':True,
    }

    return render(request,template_name=templ,context=ctx)

@login_required(login_url='utente:Login')
def acquisti(request):
    templ = 'utente/venditeAcquisti.html'
    utente = request.user
    acquisti = Acquisto.objects.filter(utente=utente).all().order_by('data')
    offerte = Offerta.objects.filter(utente=utente).all().order_by('data')
    ctx = {
        'title':'Acquisti e offerte',
        'acquisti': acquisti,
        'offerte' : offerte,
        'viewVendite':False,
    }

    return render(request,template_name=templ,context=ctx)