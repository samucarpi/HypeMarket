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

def registrazione(request):
    templ='utente/registrazione.html'
    if request.method == 'POST':
        form = Registrazione(request.POST)
        if form.is_valid() and checkPassword(form,request):
            form.save()
            messages.success(request, 'Sei stato registrato con successo!')
            return redirect('utente:Login')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Registrazione()
        return render(request,template_name=templ,context={'form':form})

def loginForm(request):
    templ='utente/login.html'
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('utente:Account')
            else:
                messages.error(request,'Email o password errati')
                return render(request,template_name=templ,context={'form':form})
        else:
            messages.error(request,'Email o password errati')
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Login()
        return render(request,template_name=templ,context={'form':form})
    
def logoutAction(request):
    logout(request)
    return redirect('prodotto:Home')
    
@login_required(login_url='utente:Login')
def account(request):
    templ='utente/account.html'
    ctx={}
    utente = request.user
    indirizzoSpedizione,indirizzoFatturazione,banca,carta=None,None,None,None
    if utente:
        if IndirizzoSpedizione.objects.filter(utente=utente).exists():
            for indirizzo in IndirizzoSpedizione.objects.filter(utente=utente):
                indirizzoSpedizione=indirizzo
        if IndirizzoFatturazione.objects.filter(utente=utente).exists():
            for indirizzo in IndirizzoFatturazione.objects.filter(utente=utente):
                indirizzoFatturazione=indirizzo
        if DatiBancari.objects.filter(utente=utente).exists():
            for banca in DatiBancari.objects.filter(utente=utente):
                banca=banca
        if CartaCredito.objects.filter(utente=utente).exists():
            for carta in CartaCredito.objects.filter(utente=utente):
                carta=carta
        ctx = {
            'utente':utente,
            'indirizzoSpedizione':indirizzoSpedizione,
            'indirizzoFatturazione':indirizzoFatturazione,
            'banca':banca,
            'carta':carta
        }
    return render(request,template_name=templ,context=ctx)

def checkInformazioni(form,request):
    if form.cleaned_data['dataNascita'] != None:
        if form.cleaned_data['dataNascita'] > time.now().date():
            messages.error(request,'Data di nascita non valida')
            return False
        if form.cleaned_data['dataNascita'].year < 1900:
            messages.error(request,'Data di nascita non valida')
            return False
        if time.now().year - form.cleaned_data['dataNascita'].year > 100:
            messages.error(request,'Data di nascita non valida')
            return False
        if time.now().year - form.cleaned_data['dataNascita'].year < 18:
            messages.error(request,'È necessario avere almeno 18 anni')
            return False
        return True
    return True

@login_required(login_url='utente:Login')
def modificaInformazioni(request):
    templ='utente/modifica.html'
    utente = request.user
    if request.method == 'POST':
        form = Informazioni(request.POST)
        if form.is_valid() and checkInformazioni(form,request):
            form.save(user=utente)
            return redirect('utente:Account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Informazioni()
        return render(request,template_name=templ,context={'form':form})

@login_required(login_url='utente:Login')
def modificaIndirizzoSpedizione(request):
    templ='utente/modifica.html'
    utente = request.user
    if request.method == 'POST':
        form = Spedizione(request.POST)
        if form.is_valid():
            if IndirizzoSpedizione.objects.filter(utente=utente).exists():
                IndirizzoSpedizione.objects.filter(utente=utente).delete()
            form.save(user=utente)
            return redirect('utente:Account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Spedizione()
        return render(request,template_name=templ,context={'form':form})
    
@login_required(login_url='utente:Login')
def modificaIndirizzoFatturazione(request):
    templ='utente/modifica.html'
    utente = request.user
    if request.method == 'POST':
        form = Fatturazione(request.POST)
        if form.is_valid():
            if IndirizzoFatturazione.objects.filter(utente=utente).exists():
                IndirizzoFatturazione.objects.filter(utente=utente).delete()
            form.save(user=utente)
            return redirect('utente:Account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Fatturazione()
        return render(request,template_name=templ,context={'form':form})

def checkBanca(form,request):
    if len(form.cleaned_data['iban']) != 27:
        messages.error(request,'IBAN non valido')
        return False
    return True

@login_required(login_url='utente:Login')
def modificaBanca(request):
    templ='utente/modifica.html'
    utente = request.user
    if request.method == 'POST':
        form = Banca(request.POST)
        if form.is_valid() and checkBanca(form,request):
            form.save(user=utente)
            return redirect('utente:Account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Banca()
        return render(request,template_name=templ,context={'form':form})
    
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
def modificaCarta(request):
    templ='utente/modifica.html'
    utente = request.user
    if request.method == 'POST':
        form = Carta(request.POST)
        if form.is_valid() and checkCarta(form,request):
            form.save(user=utente)
            return redirect('utente:Account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = Carta()
        return render(request,template_name=templ,context={'form':form})
    