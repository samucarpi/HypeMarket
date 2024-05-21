from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
import logging
from datetime import *

class Persona():
    nome=''
    cognome=''
    ruolo=''

class PersonaCreate(CreateView):
    model= Persona
    fields= ('nome','cognome','ruolo')
    template_name='tutorial/templates/persona_create.html'
    success_url = reverse_lazy('tutorial:persona-list')

logger = logging.getLogger(__name__)

def homepage(request):
    response = "Benvenuto nella Homepage, " + str(request.user)

    return HttpResponse(response)

def lista_parametri(request):
    response = ""
    for k in request.GET:
        response += request.GET[k] + " "
    return HttpResponse(response)

def info_parametri(request,nome,eta):
    out = 'Ciao: '+str(nome)+'\nHai: '+str(eta)+ ' anni'
    return HttpResponse(out, content_type="text/plain")

def utente_welcome(request,nome,eta):
    ctx={
        'title': 'Pagina di benvenuto',
        'lista': [datetime.now(),"L'ora è indicata qui su ^"] 
    }

    return render(request,template_name='utente_welcome.html',context=ctx)

def visualizza_static(request):
    return render(request,template_name='static.html')
