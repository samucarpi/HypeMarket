from django.shortcuts import render
from .models import *
from utente.models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from utente.form import *
from django.contrib.auth.decorators import login_required

def home(request):
    pagina=request.GET.get('p')
    try:
        pagina=int(pagina)
    except:
        pagina=1
    selezione_inizo=(pagina-1)*24
    selezione_fine=pagina*24
    catalogo=Prodotto.objects.all()[selezione_inizo:selezione_fine]
    paginaMax=int(len(Prodotto.objects.all())/24+1)
    templ = "prodotto/home.html"
    utente = request.user
    ctx = {
        'utente':utente,
        "title":"Catalogo sneakers", 
        "catalogo": catalogo, 
        "taglie":Taglia.objects.all(),
        'pagina':pagina,
        'paginaPiu1':pagina+1,
        'paginaPiu2':pagina+2,
        'paginaMeno1':pagina-1,
        'paginaMax':paginaMax
    }
    return render(request,template_name=templ,context=ctx)

def prodotto(request,idModello):
    templ = "prodotto/prodotto.html"

    for taglia in Taglia.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello)):
        if Proposta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').first():
            proposta = Proposta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').first()
            taglia.propostaMinore = proposta.prezzo
            Taglia.save(taglia)
        if Offerta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').last():
            offerta = Offerta.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello),taglia=taglia).order_by('prezzo').last().prezzo
            taglia.offertaMaggiore = offerta
            Taglia.save(taglia)
    
    ctx = { 
        "titolo":Prodotto.objects.get(idModello=idModello).titolo,
        "immagine":Prodotto.objects.get(idModello=idModello).immagine,
        "idModello":Prodotto.objects.get(idModello=idModello).idModello,
        "dataRilascio":Prodotto.objects.get(idModello=idModello).dataRilascio,
        "taglie":Taglia.objects.filter(prodotto=Prodotto.objects.get(idModello=idModello))
    }
    return render(request,template_name=templ,context=ctx)

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
    prodotto = Prodotto.objects.get(idModello=idModello)
    utente = request.user
    url='http://localhost:8000/sneakers/'+str(idModello)
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