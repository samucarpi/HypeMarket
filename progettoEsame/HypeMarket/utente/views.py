from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import *
from .form import *
from django.contrib.auth import authenticate
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

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
    
def checkLogin(form,request):
    if not Utente.objects.filter(email=form.cleaned_data['email']).exists():
        messages.error(request,'Email non registrata')
        return False
    utente = Utente.objects.get(email=form.cleaned_data['email'])
    if not utente.password == form.cleaned_data['password']:
        messages.error(request,'Password errata')
        return False
    return True
    
def loginForm(request):
    templ='utente/login.html'
    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid() and checkLogin(form,request):
            email = form.cleaned_data['email']
            request.session['email'] = Utente.objects.get(email=email).email
            return redirect('utente:Account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = FormLogin()
        return render(request,template_name=templ,context={'form':form})

@login_required
def account(request):
    templ='utente/account.html'
    utente = Utente.objects.get(email=request.session['email'])
    if IndirizzoSpedizione.objects.filter(utente=utente).exists():
        for indirizzo in IndirizzoSpedizione.objects.filter(utente=utente):
            via=indirizzo.via
            citta=indirizzo.citta
            cap=indirizzo.cap
            provincia=indirizzo.provincia
            nazione=indirizzo.nazione
            telefono=indirizzo.telefono
    else:
        via=citta=cap=provincia=nazione=telefono='Uknown'
    ctx = {
        'nome':utente.nome,
        'cognome':utente.cognome,
        'email':utente.email,
        'via':via,
        'citta':citta,
        'cap':cap,
        'provincia':provincia,
        'nazione':nazione,
        'telefono':telefono,
    }
    return render(request,template_name=templ,context=ctx)

@login_required
def modificaIndirizzo(request):
    templ='utente/modificaIndirizzo.html'
    user=Utente.objects.get(email=request.session['email'])
    query=IndirizzoSpedizione.objects.filter(utente=user)
    if request.method == 'POST':
        form = FormModificaIndirizzo(request.POST)
        if form.is_valid():
            if query.exists():
                query.delete()
            form.save(user=user)
            return redirect('http://localhost:8000/utente/account')
        else:
            return render(request,template_name=templ,context={'form':form})
    else:
        form = FormModificaIndirizzo()
        return render(request,template_name=templ,context={'form':form})
    
    