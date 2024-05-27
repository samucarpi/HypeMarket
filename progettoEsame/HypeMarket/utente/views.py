from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import *
from .form import *
from django.contrib.auth import authenticate
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def checkRegistrazione(form,request):
    if Utente.objects.filter(email=form.cleaned_data['email']).exists():
        messages.error(request,'Email già registrata')
        return False
    if form.cleaned_data['password'] != form.cleaned_data['confermaPassword']:
        messages.error(request,'Password non corrispondenti')
        return False
    return True

def registrazione(request):
    templ='utente/registrazione.html'
    if request.method == 'POST':
        form = FormRegistrazione(request.POST)
        if form.is_valid() and checkRegistrazione(form,request):
            form.save()
            messages.success(request, 'Sei stato registrato con successo!')
            return render(request,template_name=templ,context={'form':form})
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = FormRegistrazione()
        return render(request,template_name=templ,context={'form':form})

def loginForm(request):
    logout(request)
    templ='utente/login.html'
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password=form.cleaned_data['password']
            utente=authenticate(email=email,password=password)
            print(utente)
            if utente != None:
                login(request,utente)
                return redirect('http://localhost:8000/utente/account')
            else:
                messages.error(request,'Email o password errati')
                return render(request,template_name=templ,context={'form':form})
        else:
            messages.error(request,'Email o password errati')
            return render(request,template_name=templ,context={'form':form})
    else:
        form = FormLogin()
        return render(request,template_name=templ,context={'form':form})
    
@login_required(login_url='http://localhost:8000/utente/login')
def account(request):
    templ='utente/account.html'
    ctx={}
    indirizzoSpedizione,indirizzoFatturazione,banca,carta=None,None,None,None
    utente = request.user.id
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

def modificaIndirizzo(request):
    templ='utente/modificaIndirizzo.html'
    user=Utente.objects.get(email=request.session['email'])
    query=IndirizzoSpedizione.objects.filter(utente=user)
    if request.method == 'POST':
        form = FormModificaIndirizzo(request.POST,model=IndirizzoSpedizione)
        if form.is_valid():
            if query.exists():
                query.delete()
            form.save(user=user)
            return HttpResponseRedirect('http://localhost:8000/utente/account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = FormModificaIndirizzo()
        return render(request,template_name=templ,context={'form':form})
    
    